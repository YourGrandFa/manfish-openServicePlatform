import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from manfish_AI_Service.models.mysql_models import TmLicense, TmAccount, TmAccountLog, raw_sql_select


def permission_view(request):
    if not request.user.is_authenticated:
        # 用户未登录，重定向到登录页面或显示提示
        return redirect('login')

    if request.method == 'GET':
        username = request.user.username

        # 将结果转换为字典列表
        results = raw_sql_select("""
                SELECT a.username as username, a.account_id as account_id, b.dict_value as user_state, c.account_money as account_money, c.lock_money as lock_money, d.dict_value as account_state
                FROM tp_user a
                LEFT JOIN tb_dict b ON a.state = b.dict_id AND b.dict_type = 'user_state'
                LEFT JOIN tm_account c ON a.account_id = c.account_id
                LEFT JOIN tb_dict d ON c.state = d.dict_id AND d.dict_type = 'account_state'
                WHERE a.username = %s
            """, [username])[0]

        print(results)
        # 用户已登录，处理登录用户的逻辑
        return render(request, 'user/permission.html',
                      context={'back_url': settings.WELCOME_URL, 'user': results})

    elif request.method == 'POST':
        # 解析 JSON 数据
        comes = json.loads(request.body)

        license_code = comes['license_code']
        account_id = comes['account_id']

        # 查询当前账户状态
        account_msg = TmAccount.objects.filter(account_id=account_id).values('state', 'account_money').get()
        account_state = account_msg['state']
        account_money = account_msg['account_money']
        print(account_msg)

        # 当账户可用时
        if account_state == 1:

            # 查询该授权码是否正常在用
            license_msg = raw_sql_select("""
                select a.save_money as save_money, b.dict_value as license_state
                from tm_license a
                join tb_dict b on a.state = b.dict_id and b.dict_type = 'license_state'
                where a.license_code = %s
            """, [license_code])

            print(license_msg)
            if not license_msg:
                return JsonResponse({'status': False, 'msg': '授权码不存在'})

            license_msg = license_msg[0]
            if license_msg['license_state'] == '待使用':
                after_money = account_money + license_msg['save_money']
                log_entry = TmAccountLog(
                    order_effect_ret=0,
                    reason=f'license recharge: {license_code}',
                    account_id=account_id,
                    effect=license_msg['save_money'],
                    before=account_money,
                    after=after_money,
                    create_time=datetime.datetime.now()
                )
                log_entry.save()

                # 核销授权码
                license_updated = TmLicense.objects.filter(license_code=license_code).update(state=2)
                if license_updated:
                    # 账户余额更新
                    account_updated = TmAccount.objects.filter(account_id=account_id).update(account_money=after_money)

                return JsonResponse({'status': True, 'msg': '成功！'})

            else:
                return JsonResponse({'status': False, 'msg': '授权码已失效'})
