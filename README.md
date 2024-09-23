<<<<<<< HEAD
# manfish-openServicePlatform
This is a local service open platform based on the FastAPI+Django framework (pure Python framework), which includes two servers and two clients. It mainly serves platform service providers, opening up local computing resources (such as AI or io computing services) to customers in the form of order responses and obtaining virtual revenue from it.
=======
首先，这个系统依赖阿里云的oss存储服务，如果你不了解它，或许你需要前往它的官网
https://www.aliyun.com/product/oss

关于安装及部署：
1、你需要先理解这个架构
一个fastapi-websocket的服务商服务端（FastapiOpenServiceWebsocket）
一个websocket的服务商客户端（ClientOpenServiceWebsocket）
一个django的客户订单服务端（manfish_AI_Service）
2、使用以下指定安装必须的python模块
pip install -r requirments.txt
3、新增必要的mysql数据表
因此你需要在你的库里加载./sql目录中的sql文件
4、使用以下指定来运行这些服务
manfish_AI_Service：python manage.py runserver 0.0.0.0:9017
FastapiOpenServiceWebsocket：python websocket_openService.py
ClientOpenServiceWebsocket：python websocket_client.py

这是一些重点使用的须知
客户系统登录地址：http://127.0.0.1:9017/login
用户名：test
密码：XiG16VTU

本项目服务商客户端需要安装前置服务才能完成全覆盖支撑（ffmpeg、rembg、stable diffusion、so-vtis、GPT-soVits等），但本项目暂未提供对此的任何描述，仅供参考。
服务商服务地址：ws://127.0.0.1:9015/performer/ws/{secret}
服务商密钥secret：4rcVfCMiTEAFQodC

当前提供的服务：MP4转MP3、人物抠图、替换证件照背景色、GIF制作、渐变GIF制作、SD图片生成、歌曲翻唱、语音克隆
本次测试提供服务：MP4转MP3、人物抠图、替换证件照背景色、GIF制作、渐变GIF制作、语音克隆
提供服务需要服务商，如服务商栏目为空则代表该服务无人提供

MP4转MP3 -> 格式转换：上传mp4附件，将提取目标的声音内容并存放在MP3中反馈
人物抠图 -> 上传单张人物图片，将提供抠图服务并以原图片格式反馈（仅支持jpg、png、webp）
替换证件照背景色 -> 包括但不限于证件照，需要上传单张人物图片并在文字栏中填写目标背景颜色：red、blue、green
GIF制作 -> 一次性上传多个图片（不得超过10个且单个文件不得超过10MB），形成一个gif动图（当前版本未经审查，上传非图片格式或导致生成失败）
渐变GIF制作 -> 一次性上传多个图片（不得超过10个且单个文件不得超过10MB），形成一个渐变效果的gif动图（当前版本未经审查，上传非图片格式或导致生成失败）
SD图片生成 -> 生成后的图片未经审查，暂不提供
歌曲翻唱 -> 暂不提供
语音克隆 -> 需要上传一份音频格式的原始语音、并在文字部分填报：原始语音中文内容|期望生成语音中文内容

严重声明：本项目仅限个人学习目的，严禁商业目的。且该系统包含未经审查代码，如需参考，请详细梳理后使用，后果自负。
>>>>>>> a8b7a38 (the develope version of first.)
