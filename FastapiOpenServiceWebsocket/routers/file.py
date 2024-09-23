from sqlalchemy import func
import os
import time
from fastapi import APIRouter, Request, Header, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import urllib.parse
from model.mysql_model import TpUser, TbFileSave, TbFilePermission, TbTaskOrder
from sqlalchemy.orm import Session
import uuid
from tools import variables, dependencies as DP

router = APIRouter()


def bytes_generator(data):
    chunk_size = 1024  # 可以根据需要调整块大小
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


@router.get("/file/{file_id}")
async def robot_view(request: Request, file_id: str, db: Session = Depends(DP.get_db)):
    secret = request.headers.get("secret")
    print(secret)
    if not secret:
        raise HTTPException(status_code=403, detail="Invalid secret")

    # 检查用户是否可用
    secret_check = db.query(TpUser.user_id).filter(TpUser.secret == secret,
                                                   TpUser.state == 1).first()

    if not secret_check:
        raise HTTPException(status_code=403, detail="Permission not allowed")

    user_id = secret_check.user_id

    # 检查用户是否具有文件查阅权限
    file_get_check = db.query(TbFilePermission.id).filter(
        TbFilePermission.file_id == file_id,
        TbFilePermission.user_id == user_id
    ).first() is not None

    if not file_get_check:
        raise HTTPException(status_code=403, detail="User permission not allowed")

    file_msg = db.query(TbFileSave.file_name, TbFileSave.oss_path).filter(TbFileSave.file_id == file_id,
                                                                          TbFileSave.state == 1).first()
    print(file_msg)

    if not file_msg:
        raise HTTPException(status_code=403, detail="File not found")

    oss = variables.get_oss()
    file_seek = oss.pull_file_stream(file_msg.oss_path).read()
    file_name_encode = urllib.parse.quote(file_msg.file_name, encoding='utf-8')
    print(file_name_encode)

    return StreamingResponse(bytes_generator(file_seek), media_type="application/octet-stream",
                             headers={"Content-Disposition": f"attachment; filename={file_name_encode}"})


# 用户上传文件
@router.post("/file/upload")
async def upload_file(secret: str = Header(None), file: UploadFile = File(...),
                      db: Session = Depends(DP.get_db)):
    # 判断是否存在 secret 字段
    if secret is None:
        return {'status': False, 'msg': 'permission lost'}

    # 检查用户是否可用
    secret_check = db.query(TpUser.user_id).filter(TpUser.secret == secret, TpUser.state == 1).first()

    if not secret_check:
        raise {'status': False, 'msg': 'Permission not allowed'}

    user_id = secret_check.user_id

    # 生成file_id
    file_id = str(uuid.uuid4())  # 生成一个唯一的匿名ID
    _, file_extension = os.path.splitext(file.filename)
    file_name = str(int(time.time() * 1000)) + file_extension
    oss_path = f'OpenService/create/{file_name}'

    # 将文件保存到oss
    oss = variables.get_oss()
    upload_status = oss.upload_file_seek(file_seek=await file.read(), file_path=oss_path)
    print('upload', upload_status)

    if upload_status:
        new_file = TbFileSave(file_id=file_id, file_belong=user_id, file_name=file_name, oss_path=oss_path, state=1,
                              create_time=func.now())
        db.add(new_file)

        new_file_permission = TbFilePermission(file_id=file_id, user_id=user_id, create_time=func.now())
        db.add(new_file_permission)
        db.commit()

        # 返回唯一凭证
        return {'status': True, 'msg': file_id}
    else:
        return {'status': False, 'msg': 'update to oss failed'}


# 文件授权功能
@router.post("/file/permission/{order_id}/{file_id}")
async def file_permission(request: Request, file_id: str, order_id: str, db: Session = Depends(DP.get_db)):
    secret = request.headers.get("secret")
    print(secret)
    if not secret:
        return {'status': False, 'msg': "Invalid secret"}

    # 检查是否正常使用的用户
    secret_check = db.query(TpUser.user_id).filter(TpUser.secret == secret,
                                                   TpUser.state == 1).first()

    if not secret_check:
        return {'status': False, 'msg': "Permission not allowed"}

    user_id = secret_check.user_id

    # 检查用户是否具有文件查阅权限
    file_get_check = db.query(TbFilePermission.id).filter(
        TbFilePermission.file_id == file_id,
        TbFilePermission.user_id == user_id
    ).first() is not None

    if not file_get_check:
        return {'status': False, 'msg': "User permission not allowed"}

    # 授权给三方用户使用
    # 查询订单归属着user_id
    order_belong_user = db.query(TbTaskOrder.applyer).filter(TbTaskOrder.order_id == order_id, TbTaskOrder.performer == user_id).first()
    if not order_belong_user:
        return {'status': False, 'msg': "you can not control this order"}

    belong_user_id = order_belong_user.applyer
    new_file_permission = TbFilePermission(file_id=file_id, user_id=belong_user_id, create_time=func.now())
    db.add(new_file_permission)
    db.commit()

    return {'status': True, 'msg': "success"}

