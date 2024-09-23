import os.path

import requests
import re
from urllib.parse import unquote

headers = {'secret': '9oClySswfi3KvenX'}


def upload_file(url, file_path):
    with open(file_path, 'rb') as fi:
        file_name = os.path.basename(file_path)
        file = {'file': (file_name, fi)}
        r = requests.post(url, headers=headers, files=file)
        print(r.json())


def download_file(url, save_path):
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()  # 抛出请求错误

    # 获取原始文件名
    content_disposition = unquote(response.headers.get('Content-Disposition'))
    if content_disposition:
        # 使用正则表达式提取文件名
        matches = re.findall('filename=(?:\"(.+?)\"|(.+))', content_disposition)
        print(matches)
        if matches:
            filename = matches[0][0] or matches[0][1]
            # 如果需要，解码 URL 编码的文件名
            original_filename = unquote(filename)
        else:
            original_filename = 'downloaded_file'
    else:
        # 如果没有 Content-Disposition，使用默认的文件名
        original_filename = 'downloaded_file'

    # 将文件保存到本地
    with open(os.path.join(save_path, original_filename), 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"文件已保存为: {original_filename}")


if __name__ == '__main__':
    # file_upload_url = 'http://127.0.0.1:9015/file/upload'
    # upload_file(file_upload_url, r'response.wav')

    # 示例用法
    file_url = 'http://127.0.0.1:9015/file/acbad1ea-f82f-4fd6-ae4b-181610b03882'  # 替换为你的 FastAPI 下载链接
    save_path = ''
    download_file(file_url,'')
