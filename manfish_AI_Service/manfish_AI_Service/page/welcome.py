from django.shortcuts import HttpResponse, render, redirect
from manfish_AI_Service.models.mysql_models import TbDict


# 登录成功的确认
def welcome(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            # 查询dict_type为"welcome"的所有条目
            entries = TbDict.objects.filter(dict_type='welcome_url').values('dict_id', 'dict_value')

            # 将查询结果传递给模板
            # 如果用户已经登录并且有Session进入权限，则渲染页面
            return render(request, 'welcome/open.html',
                          context={'pages': entries, 'user': f'{username}'})
        else:
            # 用户未登录，重定向到登录页面或显示提示
            return redirect('login')


# 失败报错页面
def error_view_404(request):
    if request.method == 'GET':
        return render(request, 'error/404.html')
