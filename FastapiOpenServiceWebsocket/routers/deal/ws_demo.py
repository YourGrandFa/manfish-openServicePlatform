from fastapi import WebSocket
from model import mysql_model
from tools import variables
from sqlalchemy import update as sql_update
import datetime


order_state_change_allowed = (0, 2, 3)
process_state_allowed = (1, 2)


# 维护连接的 WebSocket 客户端列表
class ConnectionManager:
    def __init__(self, websocket: WebSocket, db):
        self.websocket = websocket
        self.db = db

    async def connect(self):
        await self.websocket.accept()

    # 下载文件
    async def download_file(self, message: str, user_id: str, is_image: bool = False):
        formatted_message = {
            'user': user_id,
            'message': message,
            'is_image': is_image
        }
        for connection, connection_id in self.active_connections.items():
            await connection.send_json(formatted_message)

    # 上传文件
    async def upload_file(self, websocket: WebSocket, message: str, user_id: str, is_image: bool = False):
        formatted_message = {
            'user': user_id,
            'message': message,
            'is_image': is_image
        }
        for connection, connection_id in self.active_connections.items():
            if connection == websocket:
                await connection.send_json(formatted_message)
                break

    # 指令解析和下发任务
    async def cmd_check(self, websocket: WebSocket, user_id: str, cmd: int, data):
        # 记录本次指令时间
        new_log = mysql_model.TpUserLog(
            user_id=user_id,
            cmd=cmd,
            create_time=datetime.datetime.now()  # 使用当前时间
        )
        self.db.add(new_log)
        self.db.commit()

        # 心跳及获取当前任务
        if cmd == 0:
            # 查询用户相关的未接受任务
            query = self.db.query(
                mysql_model.TbTaskOrder.order_id,
                mysql_model.TbTaskOrder.type_no,
                mysql_model.TbTaskOrder.desc_text,
                mysql_model.TbTaskOrder.desc_appendix,
                mysql_model.TbTaskOrder.performer
            ).filter(
                mysql_model.TbTaskOrder.performer == user_id,
                mysql_model.TbTaskOrder.state == 0
            )

            # 执行查询并获取结果
            result = self.db.execute(query.statement)

            # 转换为字典数组格式
            formatted_results1 = [dict(row) for row in result]

            # 查询用户相关的已接受任务
            query = self.db.query(
                mysql_model.TbTaskOrder.order_id,
                mysql_model.TbTaskOrder.type_no,
                mysql_model.TbTaskOrder.desc_text,
                mysql_model.TbTaskOrder.desc_appendix,
                mysql_model.TbTaskOrder.performer
            ).filter(
                mysql_model.TbTaskOrder.performer == user_id,
                mysql_model.TbTaskOrder.state == 1
            )

            # 执行查询并获取结果
            result = self.db.execute(query.statement)

            # 转换为字典数组格式
            formatted_results2 = [dict(row) for row in result]

            formatted_message = {
                'cmd': 0,
                'status': True,
                'data': {
                    'un_choice': formatted_results1,
                    'choice': formatted_results2
                }
            }
            await websocket.send_json(formatted_message)

        # 接受订单
        elif cmd == 1:
            order_id = data['order_id']
            order_now_state_base = self.db.query(mysql_model.TbTaskOrder.state).filter(mysql_model.TbTaskOrder.performer == user_id,
                                                                    mysql_model.TbTaskOrder.order_id == order_id).first()

            if not order_now_state_base:
                formatted_message = {
                    'cmd': 1,
                    'status': False,
                    'msg': f'order not found'
                }
            else:
                order_now_state = order_now_state_base.state
                if order_now_state == 0:
                    stmt = sql_update(mysql_model.TbTaskOrder).where(mysql_model.TbTaskOrder.performer == user_id, mysql_model.TbTaskOrder.order_id == order_id).values(state=1, allocate_time=datetime.datetime.now())
                    self.db.execute(stmt)
                    self.db.commit()

                    formatted_message = {
                        'cmd': 1,
                        'status': True,
                        'msg': 'success'
                    }
                else:
                    formatted_message = {
                        'cmd': 1,
                        'status': False,
                        'msg': f'order now state is {order_now_state}, not 0'
                    }
            await websocket.send_json(formatted_message)

        # 添加订单执行进程
        elif cmd == 2:
            order_id = data['order_id']
            start_time = data['start_time']
            end_time = data['end_time']
            result = data['result']
            appendix_list = data['appendix']
            if not isinstance(appendix_list, list):
                formatted_message = {
                    'cmd': 2,
                    'order_id': order_id,
                    'status': False,
                    'msg': 'your appendix not a list'
                }
                await websocket.send_json(formatted_message)
                return False

            state = data['state']

            if not (variables.check_datetime(start_time) and variables.check_datetime(end_time)):
                formatted_message = {
                    'cmd': 2,
                    'order_id': order_id,
                    'status': False,
                    'msg': 'your time format not like %Y-%m-%d %H:%M:%S'
                }
                await websocket.send_json(formatted_message)
                return False

            if state not in process_state_allowed:
                formatted_message = {
                    'cmd': 2,
                    'order_id': order_id,
                    'status': False,
                    'msg': 'your state is not allowed'
                }
                await websocket.send_json(formatted_message)
                return False

            for file_id in appendix_list:
                file_exist = self.db.query(mysql_model.TbFileSave).filter(mysql_model.TbFileSave.file_id == file_id,
                                                                        mysql_model.TbFileSave.file_belong == user_id,
                                                                        mysql_model.TbFileSave.state == 1).first() is not None
                if not file_exist:
                    formatted_message = {
                        'cmd': 2,
                        'order_id': order_id,
                        'status': False,
                        'msg': f'your file_id not allowed: {file_id}'
                    }
                    await websocket.send_json(formatted_message)
                    return False

            # 对order_id进行验证，判断用户是否有权限对这个订单做出反应
            order_exist = self.db.query(mysql_model.TbTaskOrder).filter(mysql_model.TbTaskOrder.order_id == order_id,
                                                                      mysql_model.TbTaskOrder.performer == user_id,
                                                                      mysql_model.TbTaskOrder.state == 1).first() is not None

            if not order_exist:
                formatted_message = {
                    'cmd': 2,
                    'order_id': order_id,
                    'status': False,
                    'msg': f'permission not allowed for the order: {order_id}'
                }

            else:
                new_process = mysql_model.TbTaskProces(performer=user_id, order_id=order_id, start_time=start_time,
                                                     end_time=end_time,
                                                     result=result, appendix='|'.join(appendix_list), state=state)
                self.db.add(new_process)
                self.db.commit()
                formatted_message = {
                    'cmd': 2,
                    'order_id': order_id,
                    'status': True,
                    'msg': 'done'
                }

            await websocket.send_json(formatted_message)

        # 变更订单状态
        elif cmd == 3:
            order_id = data['order_id']
            update_state = data['state']

            if update_state not in order_state_change_allowed:
                formatted_message = {
                    'cmd': 3,
                    'order_id': order_id,
                    'status': False,
                    'msg': f'state not allowed: {update_state}'
                }
            else:
                # 检查该订单是否为服务商的接受状态
                order_check = self.db.query(mysql_model.TbTaskOrder).filter(
                    mysql_model.TbTaskOrder.order_id == order_id,
                    mysql_model.TbTaskOrder.performer == user_id,
                    mysql_model.TbTaskOrder.state == 1,).first() is not None

                if not order_check:
                    formatted_message = {
                        'cmd': 3,
                        'order_id': order_id,
                        'status': False,
                        'msg': 'you have no permission to control this order'
                    }
                    await websocket.send_json(formatted_message)
                    return

                # 预设订单更新成功的回复
                formatted_message = {
                    'cmd': 3,
                    'order_id': order_id,
                    'status': True,
                    'msg': 'order state updated'
                }

                # 当要选择失败时直接更新即可
                if not update_state == 2:
                    stmt = sql_update(mysql_model.TbTaskOrder).where(mysql_model.TbTaskOrder.performer == user_id,
                                                                     mysql_model.TbTaskOrder.order_id == order_id).values(
                        state=update_state, finish_time=datetime.datetime.now())
                    self.db.execute(stmt)
                    self.db.commit()
                    await websocket.send_json(formatted_message)
                    return

                # 当要选择完结时，检查服务商是否添加进程
                process_exist = self.db.query(mysql_model.TbTaskProces).filter(mysql_model.TbTaskProces.order_id == order_id,
                                                                          mysql_model.TbTaskProces.performer == user_id).first() is not None

                if not process_exist:
                    formatted_message = {
                        'cmd': 3,
                        'order_id': order_id,
                        'status': False,
                        'msg': '未添加处理进程'
                    }
                    await websocket.send_json(formatted_message)
                    return

                # 查询订单的申请人user_id和本次订单的报酬
                order_msg = self.db.query(
                    mysql_model.TbTaskOrder.applyer,
                    mysql_model.TbTaskOrder.spend_money
                ).filter(
                    mysql_model.TbTaskOrder.order_id == order_id
                ).first()

                applyer = order_msg.applyer
                spend_money = order_msg.spend_money

                # 查询客户账户和余额
                account_id_base = self.db.query(
                    mysql_model.TpUser.account_id,
                ).filter(
                    mysql_model.TpUser.user_id == applyer
                ).first()

                account_id = account_id_base.account_id

                money_base = self.db.query(
                    mysql_model.TmAccount.lock_money,
                ).filter(
                    mysql_model.TmAccount.account_id == account_id
                ).first()
                lock_money = money_base.lock_money

                # 检查用户的冻余额是否够支付
                # 一般来说是百分之一百够的，但为了防止数据篡改刷钱，这里加上一定逻辑
                if lock_money < spend_money:
                    formatted_message = {
                        'cmd': 3,
                        'order_id': order_id,
                        'status': False,
                        'msg': 'order money not pay, you need to call system manager!'
                    }
                    await websocket.send_json(formatted_message)
                    return

                # 更新订单状态
                stmt = sql_update(mysql_model.TbTaskOrder).where(mysql_model.TbTaskOrder.performer == user_id,
                                                                 mysql_model.TbTaskOrder.order_id == order_id).values(
                    state=update_state, finish_time=datetime.datetime.now())
                self.db.execute(stmt)
                self.db.commit()

                # 客户锁定金额扣除
                new_lock_money = lock_money-spend_money
                new_account_log = mysql_model.TmAccountLog(order_effect_ret=1, order_id=order_id, reason=f'order done: {order_id}',
                                                       account_id=account_id,
                                                       effect=-spend_money, before=lock_money, after=new_lock_money,
                                                        create_time=datetime.datetime.now())
                self.db.add(new_account_log)
                self.db.commit()

                # 更新客户账户
                stmt = sql_update(mysql_model.TmAccount).where(mysql_model.TmAccount.account_id == account_id).values(
                    lock_money=new_lock_money)

                self.db.execute(stmt)
                self.db.commit()

                # 查询服务商账户和余额
                account_id_base = self.db.query(
                    mysql_model.TpUser.account_id,
                ).filter(
                    mysql_model.TpUser.user_id == user_id
                ).first()
                server_account_id = account_id_base.account_id

                money_base = self.db.query(
                    mysql_model.TmAccount.lock_money,
                ).filter(
                    mysql_model.TmAccount.account_id == server_account_id
                ).first()
                server_lock_money = money_base.lock_money

                # 计算用户最新的金额
                new_server_lock_money = server_lock_money + spend_money

                # 更新服务商的账户
                new_account_log = mysql_model.TmAccountLog(order_effect_ret=1, order_id=order_id,
                                                           reason=f'order done: {order_id}',
                                                           account_id=server_account_id,
                                                           effect=spend_money, before=server_lock_money, after=new_server_lock_money,
                                                           create_time=datetime.datetime.now())
                self.db.add(new_account_log)
                self.db.commit()

                # 更新服务商账户金额
                stmt = sql_update(mysql_model.TmAccount).where(mysql_model.TmAccount.account_id == server_account_id).values(
                    lock_money=new_server_lock_money)

                self.db.execute(stmt)
                self.db.commit()

            await websocket.send_json(formatted_message)

        # 根据order_id获取文件file_id列表
        elif cmd == 4:
            order_id = data['order_id']
            # 对order_id进行验证，判断用户是否有权限下载这个文件
            permission_exists = self.db.query(mysql_model.TbTaskOrder.desc_appendix).filter(mysql_model.TbTaskOrder.order_id == order_id,
                mysql_model.TbTaskOrder.state == 1, mysql_model.TbTaskOrder.performer == user_id).first()

            if not permission_exists:
                formatted_message = {
                    'cmd': 4,
                    'status': False,
                    'file_ids': []
                }
            else:
                file_ids = permission_exists.desc_appendix.split('|')
                formatted_message = {
                    'cmd': 4,
                    'status': True,
                    'file_ids': file_ids
                }
            await websocket.send_json(formatted_message)