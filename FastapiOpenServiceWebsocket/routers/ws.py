from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from .deal import ws_demo
from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy import update as sql_update
from model.mysql_model import TpUser, TbServiceDetail, TpUserLog
from tools import variables, dependencies as DP
import json

router = APIRouter()

# 用于跟踪每个用户的 WebSocket 连接
active_connections: Dict[str, WebSocket] = {}


@router.websocket("/performer/ws/{secret}")
async def websocket_performer(websocket: WebSocket, secret: str, db: Session = Depends(DP.get_db)):
    # 检查用户secret是否正确
    # 执行查询
    # 手动创建数据库会话,核验用户登入
    secret_check = db.query(TpUser.user_id).filter(TpUser.secret == secret, TpUser.state == 1, TpUser.user_type == 0).first()
    # 检查服务是否为在线状态
    service_online_exists = db.query(TbServiceDetail).filter(TbServiceDetail.online_state == 1,
                                                           TbServiceDetail.state == 1).first() is not None
    print(secret_check, service_online_exists)

    if not secret_check:
        await websocket.close(code=4000)
        return

    user_id = secret_check.user_id

    # 检查服务是否为在线状态
    if service_online_exists:
        if user_id in active_connections:
            # 如果用户已有连接，关闭旧连接
            try:
                old_websocket = active_connections[user_id]
                await old_websocket.send_text(json.dumps({
                    'status': False,
                    'type_no': None,
                    'msg': 'Your secret is used by other connects'
                }))
                await old_websocket.close(code=4000)
            except Exception as e:
                print(e)

        # 重置服务状态
        stmt = sql_update(TbServiceDetail).where(TbServiceDetail.user_id == user_id).values(online_state=0)
        db.execute(stmt)
        db.commit()

    # 创建一个新的连接
    active_connections[user_id] = websocket

    manager = ws_demo.ConnectionManager(websocket, db)
    await manager.connect()
    # 打开服务状态
    stmt = sql_update(TbServiceDetail).where(TbServiceDetail.user_id == user_id).values(online_state=1)
    db.execute(stmt)
    db.commit()
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            cmd = data.get('cmd')
            await manager.cmd_check(websocket, user_id, cmd, data)

    except Exception as e:
       print(e)
    finally:
       # 退出服务在线状态
       stmt = sql_update(TbServiceDetail).where(TbServiceDetail.user_id == user_id).values(online_state=0)
       db.execute(stmt)
       db.commit()

       if user_id in active_connections:
           del active_connections[user_id]