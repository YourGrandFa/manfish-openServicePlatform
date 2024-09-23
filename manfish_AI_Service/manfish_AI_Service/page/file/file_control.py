import os
import time

from django.http import HttpResponse
from django.conf import settings
import urllib.parse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from manfish_AI_Service.models import api_models
from manfish_AI_Service.models.mysql_models import TpUser, TbFilePermission, TbFileSave

APPENDIX_SAVE_PATH = settings.APPENDIX_SAVE_PATH
DOWNLOAD_SAVE_PATH = settings.DOWNLOAD_SAVE_PATH


# 文件上传
def file_upload(request):
    if not request.user.is_authenticated:
        # 用户未登录，重定向到登录页面或显示提示
        return redirect('login')

    if request.method == 'POST':
        username = request.user.username

        user_msg = TpUser.objects.filter(username=username, state=1).values('secret')
        secret = user_msg[0]['secret']

        files = request.FILES.getlist('files')
        print('收到文件数量', len(files))

        file_ids = []
        # 限制文件数量
        if len(files) > 10:
            return JsonResponse({'status': False, 'msg': '最多只能上传10个文件'})

        # 限制文件大小
        max_file_size = 10 * 1024 * 1024  # 10MB
        for file in files:
            if file.size > max_file_size:
                return JsonResponse({'status': False, 'msg': f'文件 {file.name} 超过最大大小限制 10MB'})

        for file in files:
            # 保存文件
            file_name = file.name

            # 拿取上传文件后缀
            file_name_parts = os.path.splitext(file_name)
            file_extension = file_name_parts[1]  # 后缀名部分

            save_path = os.path.join(APPENDIX_SAVE_PATH, f'{int(time.time() * 1000)}{file_extension}')
            with open(save_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            result = api_models.upload_file(secret, save_path)
            print(result)
            if result['status']:
                file_id = result['msg']

                # 如果存放成功则匹配本地存储地址给这个file_id
                TbFileSave.objects.filter(file_id=file_id).update(local_save_path=save_path)
                file_ids.append(file_id)
            else:
                return JsonResponse({'status': False, 'msg': '文件上传失败'})

        return JsonResponse({'status': True, 'msg': '|'.join(file_ids)})


# 文件下载
def file_download(request):
    if not request.user.is_authenticated:
        # 用户未登录，重定向到登录页面或显示提示
        return redirect('login')

    if request.method == 'GET':
        username = request.user.username

        file_id = request.GET.get('file_id')
        if file_id is None:
            return HttpResponse('File not found', status=404)

        # 拿取用户secret秘钥
        user_msg = TpUser.objects.filter(username=username, state=1).values('secret', 'user_id')[0]
        secret = user_msg['secret']
        user_id = user_msg['user_id']

        # 查询用户是否有权限访问该文件
        file_permission = TbFilePermission.objects.filter(user_id=user_id, file_id=file_id)
        if not file_permission:
            return HttpResponse('Permission not allowed', status=404)

        # 查询文件本地路径以及文件名
        file_msg = TbFileSave.objects.filter(file_id=file_id).values('file_name', 'local_save_path')[0]
        file_name = file_msg['file_name']

        local_save_path = file_msg['local_save_path']
        print(file_msg)
        # 看看这个附件是否已在本地存储
        if local_save_path and os.path.exists(local_save_path):
            file_path = local_save_path
        # 没有的话就尝试拉取最新的文件
        else:
            file_path = os.path.join(DOWNLOAD_SAVE_PATH, file_name)
            ret = api_models.download_file(secret, file_id, file_path)
            if ret:
                # 更新最新的本地地址
                TbFileSave.objects.filter(file_id=file_id).update(local_save_path=file_path)
                print(f"文件已保存在: {file_path}")

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
        response[
            'Content-Disposition'] = f'''attachment; filename="{urllib.parse.quote(file_name.encode('utf-8'))}"'''
        return response
    else:
        return HttpResponse('File not found', status=404)
