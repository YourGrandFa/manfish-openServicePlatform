import asyncio
import json
import logging
import time
import websockets
from tools import file_operate, order_operate, log_deal
from multiprocessing import Process, Queue
import configparser

lock = asyncio.Lock()

service_links = {
    'mp42mp3': 1,
    'man_cut': 2,
    'replace_bg_color': 3,
    'gif_create': 4,
    'gif_pro_create': 5,
    'sd': 6,
    'music_cover': 7,
    'tts_cover': 8,
}

# 不需要附件的服务编号
APPENDIX_NEEDLESS = [6]

CONF = configparser.ConfigParser()
CONF.read('client.ini')
GLOBAL_CONF = CONF['global']
api_home = GLOBAL_CONF['api_home']
secret = GLOBAL_CONF['secret']
SERVICE_CONF = CONF['service']
FILE_PATH = CONF['file_path_windows']
UPLOAD_PAHT = FILE_PATH['upload']
CREATE_PATH = FILE_PATH['create']

ALIVE_SERVICE = ()
# 对将要开启的服务进行检查
for service_name in service_links:
    if SERVICE_CONF[service_name].replace(' ', '') == '1':
        ALIVE_SERVICE += (service_links[service_name],)
print(ALIVE_SERVICE)

# 创建一个日志器。提供控制台和日志输出
# 这个日志允许控制台输出
LOGGER = log_deal.get_logger(FILE_PATH['log'], level=logging.WARNING, when='D', back_count=0)

# 已接任务全局
CHECK_TASKS = []
# 当前执行程序全局，为避免资源并发，每次只能运行一个
# 但是由于当前为单进程执行，因为这里并暂没有发挥用处
PROCESS_AUTO_ALLOW = True
# 服务同一时间允许接受量全局
MAX_ORDER_ALLOW = int(SERVICE_CONF['max_order_allow'])

server_http_url = f"http://{api_home}"


# 通用处理结果反馈
async def public_operate_dead(queue, update_state, order_id, start_time, result, appendix):
    if update_state == 2:
        state = 1
    else:
        state = 2

    await queue.put(
        {
            "cmd": 2,
            "order_id": order_id,
            "start_time": start_time,
            "end_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "result": result,
            "state": state,
            "appendix": appendix
        }
    )
    await queue.put(
        {
            "cmd": 3,
            "order_id": order_id,
            "state": update_state,
        }
    )


# 服务运行
async def service_control(queue):
    global CHECK_TASKS
    global PROCESS_AUTO_ALLOW
    while True:
        if CHECK_TASKS and PROCESS_AUTO_ALLOW:
            print('here', CHECK_TASKS)
            next_task = CHECK_TASKS[0]
            order_id = next_task['order_id']

            # 创建队列以收集进程结果
            process_queue = Queue()

            p = Process(target=order_operate.master_control, args=(APPENDIX_NEEDLESS, server_http_url, UPLOAD_PAHT, CREATE_PATH, secret, next_task, process_queue))
            p.start()
            p.join()

            if not process_queue.empty():
                ret, msg = process_queue.get()
                await public_operate_dead(queue, msg[0], msg[1], msg[2], msg[3], msg[4])
                LOGGER.debug(f"{order_id} {ret}: {msg[3]} - {msg[4]}")
                del CHECK_TASKS[0]

        await asyncio.sleep(1)


async def send_messages(websocket, queue):
    while True:
        message = await queue.get()
        await websocket.send(json.dumps(message))
        print(f"Sent: {message}")


async def send_heartbeat(websocket):
    while True:
        try:
            # 发送心跳消息
            heartbeat_message = {'cmd': 0}
            # await websocket.send(json.dumps(heartbeat_message), timeout=3)
            await asyncio.wait_for(websocket.send(json.dumps(heartbeat_message)), timeout=3)
            print(f"Sent heartbeat: {heartbeat_message}")

            # 等待 10 秒
            await asyncio.sleep(10)
        except Exception as e:
            print(e)
            await asyncio.sleep(2)


async def receive_messages(websocket):
    global CHECK_TASKS
    try:
        async for message in websocket:
            try:
                # 解析 JSON 消息
                data = json.loads(message)
                print(data)
                if data['cmd'] == 0 and data['status']:
                    choices = data['data']
                    if choices['un_choice']:
                        for choice in choices['un_choice']:
                            type_no = choice['type_no']
                            # 先检查服务类型是否被本机支持
                            if type_no in ALIVE_SERVICE:
                                # 禁止压入超过MAX_ORDER_ALLOW数量要求的过多任务
                                if len(CHECK_TASKS) < MAX_ORDER_ALLOW:
                                    CHECK_TASKS.append(choice)
                                    LOGGER.debug(f"CHECK_TASKS add: {choice['order_id']}")
                                    await websocket.send(json.dumps({
                                        "cmd": 1, "order_id": choice['order_id']
                                    }))

                    if choices['choice']:
                        for choice in choices['choice']:
                            # 当出现无名服务时，考虑为上个运行脚本的中断，因此将订单状态重新更改为0
                            if choice not in CHECK_TASKS:
                                order_id = choice['order_id']
                                await asyncio.wait_for(
                                    websocket.send(json.dumps({"cmd": 3, "order_id": order_id, "state": 0})), timeout=3)
                                LOGGER.debug(f"reback order: {order_id}")

                elif data['cmd'] == 3:
                    LOGGER.warning(f"{data['order_id']} updated: {data['status']} {data['msg']}")

                elif data['cmd'] == 2:
                    LOGGER.warning(f"{data['order_id']} process add: {data['status']} {data['msg']}")

                elif data['cmd'] == 4:
                    LOGGER.warning(f"{data['order_id']} get files: {data['status']} {data['file_ids']}")

            except json.JSONDecodeError:
                print("Received non-JSON message")
    except websockets.ConnectionClosed:
        print("websocket lost! receive_messages dead.")
    except Exception as e:
        print(f"{e}!receive_messages dead")


async def main(url):
    async with websockets.connect(url) as websocket:
        LOGGER.debug('websocket connected!')
        queue = asyncio.Queue()

        # 启动发送消息、发送心跳和接收消息、功能脚本操作的任务
        service_control_task = asyncio.create_task(service_control(queue))
        send_task = asyncio.create_task(send_messages(websocket, queue))
        heartbeat_task = asyncio.create_task(send_heartbeat(websocket))
        receive_task = asyncio.create_task(receive_messages(websocket))

        # 等待所有任务完成（实际上这里的任务会永远运行）
        # await asyncio.gather(send_task, heartbeat_task, receive_task)
        LOGGER.debug('all tasks started!')

        await receive_task

        service_control_task.cancel()
        send_task.cancel()
        heartbeat_task.cancel()
        receive_task.cancel()
        LOGGER.warning('websocket lost')


if __name__ == '__main__':
    # WebSocket 服务器地址
    url = f"ws://{api_home}/performer/ws/{secret}"
    print(url)

    # 运行客户端
    asyncio.run(main(url))
