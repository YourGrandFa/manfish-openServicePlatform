import os
import django

# 设置 Django 项目的环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manfish_AI_Service.settings")
django.setup()

from django.contrib.auth.models import User


def create_user(username, email, password):
    # 检查用户是否已经存在
    if User.objects.filter(username=username).exists():
        print(f"用户 '{username}' 已经存在")
        return

    # 创建新用户
    User.objects.create_user(username=username, email=email, password=password)
    print(f"用户 '{username}' 创建成功")


def update_user_password(username, old, new):
    # 检查用户是否已经存在
    user = User.objects.get(username=username)

    if user:
        # 验证旧密码
        if user.check_password(old):
            # 旧密码正确，设置新密码
            user.set_password(new)
            user.save()
            print(f"Password for user '{username}' changed successfully.")
        else:
            print("Old password is incorrect.")
    else:
        print('username not found')


def delete_user(username):
    # 查找用户
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"User '{username}' deleted successfully.")
    except User.DoesNotExist:
        print(f"User '{username}' does not exist.")


if __name__ == "__main__":
    # 替换为你想要创建的用户信息
    username = "dhl"
    email = "xxx@qq.com"
    password = "KveJr4mI"
    # new_password = 'xxxxx'

    create_user(username, email, password)
    # update_user_password(username, password, new_password)
    # delete_user('dhl')