from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login


def user_input_check(username, password):
    message = ''
    if len(username) > 16:
        message = "用户名不得超过16位！"
    elif len(password) < 6:
        message = "密码不得少于6位！"
    elif len(password) > 16:
        message = "密码不得超过16位！"
    if message:
        return False, message
    else:
        return True, ''


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        ret, msg = user_input_check(username, password)
        if ret:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/welcome')  # 替换 'welcome' 为你应用的主页视图名
            else:
                messages.error(request, "用户名或密码错误！")
        else:
            messages.error(request, msg)

    return render(request, 'user/login.html')
