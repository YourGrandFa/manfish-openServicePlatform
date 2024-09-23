import datetime
import json

from django.db.models import F, FloatField, ExpressionWrapper, DecimalField
from django.db.models.functions import Round
from django.shortcuts import render, redirect
from django.conf import settings
from manfish_AI_Service.models.mysql_models import TbServiceType, raw_sql_select, TbServiceDetail, TpUser, TbTaskOrder, TmAccountLog, TmAccount, TbFilePermission, TbFileSave
from django.http import JsonResponse


def service_list_view(request):
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

        service_types = raw_sql_select("""
        SELECT   a.type_no as type_no,
            a.service_name as service_name,
            a.service_desc as service_desc,
            a.price as price,
            COALESCE(b.service_count, 0) AS service_count  -- 用 COALESCE 将 NULL 变为 0
        FROM 
            tb_service_type a
        LEFT JOIN 
            (SELECT type_no, COUNT(*) AS service_count 
             FROM tb_service_detail 
             WHERE state = 1 
             GROUP BY type_no) b 
        ON 
            a.type_no = b.type_no
        WHERE 
            a.state = 1
        order by a.type_no, service_count desc;
        """, [])

        # 用户已登录，处理登录用户的逻辑
        return render(request, 'service/service_list.html',
                      context={'back_url': settings.WELCOME_URL, 'user': user_msg, 'services': service_types})


def service_detail_view(request):
    if not request.user.is_authenticated:
        # 用户未登录，重定向到登录页面或显示提示
        return redirect('login')

    if request.method == 'GET':
        type_no = request.GET['type_no']
        service_msg = TbServiceType.objects.filter(type_no=type_no).values('type_no', 'service_name', 'service_desc', 'price')[0]

        # 获取符合条件的用户信息，并按 success_done 排序
        servers = (
            TpUser.objects
                .filter(user_id__in=TbServiceDetail.objects.filter(type_no=type_no, state=1, online_state=1)
                        .values_list('user_id', flat=True))  # 获取符合条件的 user_id 列表
                .annotate(
                    success_rate=Round(
                    ExpressionWrapper(
                        F('success_done') / F('all_done') * 100,
                        output_field=FloatField()
                    ),
                    1  # 保留一位小数
                )
            )
                .values('user_id', 'username', 'all_done', 'success_done', 'bad_done', 'success_rate')
                .order_by('-success_done')  # 按 success_done 字段降序排序
        )

        # 用户已登录，处理登录用户的逻辑
        return render(request, 'service/service_detail.html',
                      context={'back_url': settings.WELCOME_URL, 'service': service_msg, 'servers': servers, 'type_no': type_no})

    elif request.method == 'POST':
        username = request.user.username
        
        comes = json.loads(request.body)
        file_str = comes['file_str']
        desc_text = comes['desc_text']
        type_no = comes['type_no']
        performer = comes['performer']

        # 如果订单类型为空，或者 文件列表和附件描述均不存在时， 考虑为非法请求
        if not type_no or not (file_str or desc_text):
            return JsonResponse({'status': False, 'msg': 'permission not allowed'})

        # 先检查用户是否有足够的资本发起订单
        service_msg = TbServiceType.objects.filter(type_no=type_no).values('price')[0]
        price = service_msg['price']

        user_msg = raw_sql_select("""
            select a.user_id as user_id, b.account_id as account_id, b.account_money as money
            from tp_user a 
            join tm_account b on a.account_id = b.account_id 
            where a.username = %s
            """, [username])
        user_msg = user_msg[0]
        user_id = user_msg['user_id']
        user_money = user_msg['money']
        account_id = user_msg['account_id']

        if user_money < price:
            return JsonResponse({'status': False, 'msg': '您的余额已不足，请及时充值'})

        # 检查用户是否有对这些文件的归属权利
        for file_id in file_str.split('|'):
            file_permission = TbFileSave.objects.filter(file_id=file_id, state=1).values('file_belong')[0]
            if file_permission['file_belong'] != user_id:
                return JsonResponse({'status': False, 'msg': '该附件并非为请求者的拥有者'})

        # 赋予服务商附件访问能力
        for file_id in file_str.split('|'):
            new_order = TbFilePermission(
                file_id=file_id,
                user_id=performer,
                create_time=datetime.datetime.now(),
            )
            new_order.save()

        # 订单存入
        now_time = datetime.datetime.now()
        new_order = TbTaskOrder(
            type_no=type_no,
            desc_text=desc_text,
            desc_appendix=file_str,
            applyer=user_id,
            apply_time=now_time,
            create_time=now_time,
            performer=performer,
            spend_money=price,
            state=0
        )
        new_order.save()

        # 获取自增长的 ID
        order_id = new_order.order_id

        # 如果订单被接受则开始冻结用户本次使用的费用
        if order_id:
            after_money = user_money - price
            log_entry = TmAccountLog(
                order_effect_ret=0,
                reason=f'add order: {order_id}',
                account_id=account_id,
                effect=0-price,
                before=user_money,
                after=after_money,
                create_time=datetime.datetime.now()
            )
            log_entry.save()

            # 账户余额更新
            TmAccount.objects.filter(account_id=account_id).update(account_money=after_money, lock_money=F('lock_money')+price)
            return JsonResponse({'status': True, 'msg': order_id})
        else:
            return JsonResponse({'status': False, 'msg': '订单创建失败'})