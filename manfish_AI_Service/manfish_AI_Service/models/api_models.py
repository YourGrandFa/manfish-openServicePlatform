import re
from urllib.parse import unquote
import requests
import os
from django.conf import settings

SERVICE_API_URL = settings.SERVICE_API_URL


# 文件上传
def upload_file(secret, file_path):
    result = {'status': False}
    try:
        with open(file_path, 'rb') as fi:
            file_name = os.path.basename(file_path)
            files = {'file': (file_name, fi)}
            headers = {'secret': secret}
            r = requests.post(SERVICE_API_URL + '/file/upload', files=files, headers=headers)
            result = r.json()
    except Exception as e:
        print(e)
    finally:
        return result


def download_file(secret, file_id, file_path):
    ret = False
    try:

        # 如果该文件已存在，就没必要下载了
        if not os.path.exists(file_path):
            headers = {'secret': secret}
            response = requests.get(SERVICE_API_URL + f'/file/{file_id}', headers=headers, stream=True)
            response.raise_for_status()  # 抛出请求错误

            # 将文件保存到本地
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        ret = True
    except Exception as e:
        print(e)
    finally:
        return ret
