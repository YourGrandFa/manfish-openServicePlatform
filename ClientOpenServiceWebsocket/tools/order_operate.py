import subprocess
import os
import re
import time
from urllib.parse import unquote
from PIL import Image, ImageSequence
import requests

TTS_COVER_API = 'http://127.0.0.1:9880/tts'


def master_control(APPENDIX_NEEDLESS, server_http_url, UPLOAD_PAHT, CREATE_PATH, secret, next_task, queue):
    order_id = next_task['order_id']
    type_no = next_task['type_no']
    desc_text = next_task['desc_text']
    desc_appendix = next_task['desc_appendix']
    start_time = time.strftime('%Y-%m-%d %H:%M:%S')

    create_files = []
    result_text = ""

    # 检查是否是必须下载附件的服务
    if type_no not in APPENDIX_NEEDLESS:
        # 尝试下载附件
        save_paths = download_appendix(server_http_url, UPLOAD_PAHT, secret, desc_appendix)
        if not save_paths:
            queue.put((False, (3, order_id, start_time, "附件下载失败", [])))

        else:
            if type_no == 1:
                for save_path in save_paths:
                    ret, mp3_path = mp42mp3(save_path, CREATE_PATH)
                    if ret:
                        create_files.append(mp3_path)
            elif type_no == 2:
                for save_path in save_paths:
                    ret, file_path = man_cut(save_path, CREATE_PATH)
                    if ret:
                        create_files.append(file_path)
            elif type_no == 3:
                if desc_text not in ('red', 'blue', 'green'):
                    queue.put((False, (3, order_id, start_time, "颜色选择不正确", [])))

                for save_path in save_paths:
                    ret, file_path = replace_bg_color(save_path, CREATE_PATH, )
                    if ret:
                        create_files.append(file_path)

            elif type_no == 4:
                ret, file_path = gif_create(save_paths, CREATE_PATH)
                if ret:
                    create_files = [file_path]

            elif type_no == 5:
                ret, file_path = gif_pro_create(save_paths, CREATE_PATH)
                if ret:
                    create_files = [file_path]

            elif type_no == 8:
                text_split = desc_text.split('|')
                if len(text_split) < 2:
                    queue.put((False, (3, order_id, start_time, "请注明音频提示词和想要输入的内容！", "")))

                refer_tts = text_split[0]
                text = '|'.join(text_split[1:])
                ret, file_path = tts_cover(CREATE_PATH, save_paths[0], refer_tts, text)
                if ret:
                    create_files = [file_path]

    if result_text or create_files:
        result_files = upload_file(server_http_url, secret, create_files)
        for file_id in result_files:
            permission_file(server_http_url, secret, order_id, file_id)
        queue.put((True, (2, order_id, start_time, result_text, result_files)))

    queue.put((False, (3, order_id, start_time, "", "")))


# 下载订单附件
def download_appendix(server_http_url, CREATE_PATH, secret, desc_appendix):
    headers = {'secret': secret}

    save_paths = []
    for file_id in desc_appendix.split('|'):
        try:
            url = server_http_url + f'/file/{file_id}'
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

            save_path = os.path.join(CREATE_PATH, original_filename)
            # 将文件保存到本地
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"文件已保存为: {original_filename}")
            save_paths.append(save_path)
        except Exception as e:
            print(e)
    return save_paths


# 上传文件
def upload_file(server_http_url, secret, file_paths):
    headers = {'secret': secret}
    backs = []
    for file_path in file_paths:
        with open(file_path, 'rb') as fi:
            file_name = os.path.basename(file_path)
            file = {'file': (file_name, fi)}
            r = requests.post(server_http_url + f'/file/upload', headers=headers, files=file)
            result = r.json()
            if result['status']:
                backs.append(result['msg'])
    return backs

# 文件授权
def permission_file(server_http_url, secret, order_id, file_id):
    headers = {'secret': secret}
    response = requests.post(server_http_url + f'/file/permission/{order_id}/{file_id}', headers=headers)
    print(response)


# mp4转mp3
def mp42mp3(mp4_path, CREATE_PATH):
    ret = False
    mp3_path = os.path.join(CREATE_PATH, f"{int(time.time())}.mp3")
    try:
        command = ['ffmpeg', '-i', mp4_path, '-vn', '-acodec', 'libmp3lame', mp3_path]
        subprocess.run(command)
        ret = True
    except Exception as e:
        print(e)
    finally:
        return ret, mp3_path


# 人物抠图
def man_cut(before_path, CREATE_PATH):
    ret = False
    _, file_extension = os.path.splitext(before_path)
    # 检查是否是符合条件的图片格式
    if file_extension not in ('.jpg', '.png', '.webp'):
        return False, ""

    after_path = os.path.join(CREATE_PATH, f"{int(time.time())}{file_extension}")
    try:
        command = ['rembg', 'i', before_path, after_path]
        subprocess.run(command)
        ret = True
    except Exception as e:
        print(e)
    finally:
        return ret, after_path


# 替换背景色
def replace_bg_color(before_path, CREATE_PATH, color='red'):
    pure_ret, pure_path = man_cut(before_path, CREATE_PATH)
    ret = False
    after_path = ''
    try:
        if pure_ret:
            _, file_extension = os.path.splitext(pure_path)
            # 检查是否是符合条件的图片格式
            after_path = os.path.join(CREATE_PATH, f"{int(time.time())}{file_extension}")

            # 加上背景颜色
            no_bg_image = Image.open(pure_path)
            x, y = no_bg_image.size
            new_image = Image.new('RGBA', no_bg_image.size, color=color)
            new_image.paste(no_bg_image, (0, 0, x, y), no_bg_image)
            new_image.save(after_path)
            ret = True
    except Exception as e:
        print(e)
    finally:
        return ret, after_path


# gif制作
def gif_create(before_paths: list, CREATE_PATH, speed=1000):
    ret = False
    after_path = os.path.join(CREATE_PATH, f"{int(time.time())}.gif")
    try:
        # 定义幕布尺寸
        before_img_path = before_paths[0]
        before_img = Image.open(before_img_path)
        gif_size = before_img.size

        # 创建输出图片序列
        images = []
        for img_path in before_paths[1:]:
            image = Image.open(img_path).resize(gif_size)
            images.append(image)

        # 保存过渡帧为GIF动图
        before_img.save(after_path, save_all=True, append_images=images, optimize=False, duration=speed, loop=0)
        ret = True
    except Exception as e:
        print(e)
    finally:
        return ret, after_path


def gif_pro_create(before_paths: list, CREATE_PATH, cuts=15, speed=100):
    ret = False
    after_path = os.path.join(CREATE_PATH, f"{int(time.time())}.gif")
    try:
        # 定义幕布尺寸
        before_img_path = before_paths[0]
        before_img = Image.open(before_img_path)
        gif_size = before_img.size
        # 创建输出图片序列
        frames = []
        # 定义过渡帧数
        num_frames = cuts

        for img_path in before_paths[1:]:
            image = Image.open(img_path).resize(gif_size)

            # 生成过渡帧
            for i in range(num_frames + 1):
                # 计算混合比例
                alpha = i / num_frames

                # 通过混合两张图片生成过渡帧
                blended_image = Image.blend(before_img, image, alpha)

                # 将过渡帧添加到输出序列中
                frames.append(blended_image)

            # 更新渐变前图
            before_img = image

        # 保存过渡帧为GIF动图
        frames[0].save(after_path, save_all=True, append_images=frames[1:], optimize=False, duration=speed, loop=0)
        ret = True
    except Exception as e:
        print(e)
    finally:
        return ret, after_path


# GPT-SoVITS声音克隆
def tts_cover(CREATE_PATH, refer_music, refer_tts, text):
    after_path = os.path.join(CREATE_PATH, f"{int(time.time())}.wav")
    ret = False
    try:
        data = {
            "text": text,
            "text_lang": "all_zh",
            "ref_audio_path": os.path.abspath(refer_music),
            "prompt_text": refer_tts,
            "prompt_lang": "all_zh",
            "speed_factor": 1.0,
            "seed": -1,
            "parallel_infer": True
        }
        r = requests.post(TTS_COVER_API, json=data)
        result = r.content
        with open(after_path, 'wb') as file:
            file.write(result)
        ret = True
    except Exception as e:
        print(e)
    finally:
        return ret, after_path

if __name__ == '__main__':
    # result = gif_create(['特朗普1.webp', '特朗普2.webp', '特朗普3.webp'], '')
    # print(result)

    # result = tts_cover('', r'E:\PycharmProjects\ClientOpenServiceWebsocket\file_home\upload\1725562360000.wav', "你的微笑，如毒药，让我深深着迷，却又害怕沉沦...", "我真的好爱你吖~到底怎么才能获得你呢?")
    # print(result)

    permission_file('http://127.0.0.1:9015', '4rcVfCMiTEAFQodC', 12, 'acbad1ea-f82f-4fd6-ae4b-181610b03882')