from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.conf import settings
from manfish_AI_Service.models.mysql_models import TbServiceType, raw_sql_select, TbFileSave


def order_list_view(request):
    if not request.user.is_authenticated:
        # 用户未登录，重定向到登录页面或显示提示
        return redirect('login')

    if request.method == 'GET':
        username = request.user.username
        user_msg = raw_sql_select("""
        select a.username as username, b.account_money as money
        from tp_user a 
        join tm_account b on a.account_id = b.account_id 
        where a.username = %s
        """, [username])
        user_msg = user_msg[0]

        orders = raw_sql_select("""
        select a.order_id as order_id, c.service_name as service_name, a.spend_money as spend_money, e.username as performer, date_format(a.apply_time, '%%Y-%%m-%%d %%H:%%i') as apply_time, date_format(a.finish_time, '%%Y-%%m-%%d %%H:%%i') as finish_time, d.dict_value as state 
        from tp_user b
        join tb_task_order a on a.applyer = b.user_id
        join tp_user e on a.performer = e.user_id
        join tb_service_type c on a.type_no = c.type_no
        join tb_dict d on a.state = d.dict_id and d.dict_type = 'order_state'
        where b.username = %s order by a.apply_time desc
        """, [user_msg['username']])

        paginator = Paginator(orders, 5)  # 每页显示5个项目
        page_number = request.GET.get('page', 1)  # 获取当前页码
        page_obj = paginator.get_page(page_number)  # 获取分页后的 Page 对象

        # 用户已登录，处理登录用户的逻辑
        return render(request, 'order/order_list.html',
                      context={'back_url': settings.WELCOME_URL, 'user': user_msg, 'page_obj': page_obj})


def order_detail_view(request):
    if not request.user.is_authenticated:
        # 用户未登录，重定向到登录页面或显示提示
        return redirect('login')

    if request.method == 'GET':
        username = request.user.username
        order_id = request.GET['order_id']

        # 附件内容
        order_msg = raw_sql_select("""
        select c.service_name as service_name, a.spend_money as spend_money, a.desc_text as desc_text, a.desc_appendix as desc_appendix, e.username as performer, date_format(a.apply_time, '%%Y-%%m-%%d %%H:%%i') as apply_time, date_format(a.finish_time, '%%Y-%%m-%%d %%H:%%i') as finish_time, d.dict_value as state 
        from tp_user b
        join tb_task_order a on a.applyer = b.user_id
        join tp_user e on a.performer = e.user_id
        join tb_service_type c on a.type_no = c.type_no
        join tb_dict d on a.state = d.dict_id and d.dict_type = 'order_state'
        where b.username = %s and a.order_id = %s
        """, [username, order_id])[0]
        print(order_msg)

        file_names = []
        if order_msg['desc_appendix']:
            file_names = TbFileSave.objects.filter(file_id__in=order_msg['desc_appendix'].split('|')).values('file_id', 'file_name')
        order_msg['file_names'] = file_names

        # 查询执行进程
        processes = raw_sql_select("""
        SELECT 
            e.dict_value as state, 
            c.result as res_text, 
            c.appendix as appendix,
            date_format(c.end_time, '%%Y-%%m-%%d %%H:%%i') as process_time
        FROM 
            tb_task_process c
        JOIN 
            tb_dict e ON c.state = e.dict_id AND e.dict_type = 'process_state'
        WHERE 
            c.order_id = %s 
        """, [order_id])
        print(processes)
        for index, process in enumerate(processes):
            file_names = []
            if process['appendix']:
                appendixes = process['appendix'].split('|')
                file_names = TbFileSave.objects.filter(file_id__in=appendixes).values('file_id', 'file_name')
            processes[index]['file_names'] = file_names

        # 映射订单详情信息到前端页面
        return render(request, 'order/order_detail.html',
                      context={'back_url': settings.WELCOME_URL, 'order_msg': order_msg, 'processes': processes})