"""manfish_AI_Service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views import static as sta  # 新增
from .page.user import login, permission
from .page import welcome
from .page.service import service_control
from .page.file import file_control
from .page.order import order_control

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', sta.serve,
            {'document_root': 'static'}, name='static'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('login/', login.login_view, name='login'),
    path('error/404', welcome.error_view_404, name='404'),
    path('welcome', welcome.welcome, name='welcome'),

    path('person/permission', permission.permission_view, name='permission'),

    path('service/home', service_control.service_list_view, name='service_list'),
    path('service/detail', service_control.service_detail_view, name='service_detail'),

    path('file/upload', file_control.file_upload, name='file_upload'),
    path('file/download', file_control.file_download, name='file_download'),

    path('order/list', order_control.order_list_view, name='order_list'),
    path('order/detail', order_control.order_detail_view, name='order_detail'),
]
