# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbDict(models.Model):
    dict_type = models.CharField(max_length=255, blank=True, null=True, db_comment='服务器或区域、其他描述')
    dict_id = models.CharField(max_length=255, blank=True, null=True, db_comment='字典id、名称、代指词')
    dict_value = models.CharField(max_length=255, blank=True, null=True, db_comment='目标值')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')

    class Meta:
        managed = False
        db_table = 'tb_dict'


class TbFilePermission(models.Model):
    file_id = models.CharField(max_length=255, blank=True, null=True, db_comment='文件编号')
    user_id = models.IntegerField(blank=True, null=True, db_comment='用户编号')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')

    class Meta:
        managed = False
        db_table = 'tb_file_permission'


class TbFileSave(models.Model):
    file_id = models.CharField(primary_key=True, max_length=255, db_comment='文件id')
    file_belong = models.IntegerField(blank=True, null=True, db_comment='文件归属者user_id')
    file_name = models.CharField(max_length=255, blank=True, null=True, db_comment='文件名称')
    local_save_path = models.TextField(blank=True, null=True, db_comment='本地存储地址')
    oss_path = models.TextField(blank=True, null=True, db_comment='阿里云oss存储地址')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    state = models.IntegerField(blank=True, null=True, db_comment='当前状态，0为禁止访问，1为允许访问')

    class Meta:
        managed = False
        db_table = 'tb_file_save'


class TbServiceDetail(models.Model):
    service_id = models.AutoField(primary_key=True, db_comment='服务id')
    user_id = models.IntegerField(blank=True, null=True, db_comment='服务者/执行者user_id')
    type_no = models.IntegerField(blank=True, null=True, db_comment='任务类型编号')
    online_state = models.IntegerField(blank=True, null=True, db_comment='服务上线状态，0离线，1在线')
    state = models.IntegerField(blank=True, null=True, db_comment='服务状态，0未部署，1已部署，2已下架，3已清除，4正在维护')

    class Meta:
        managed = False
        db_table = 'tb_service_detail'
        db_table_comment = '服务资源清单'


class TbServiceType(models.Model):
    type_no = models.AutoField(primary_key=True, db_comment='服务编号')
    service_name = models.CharField(max_length=255, blank=True, null=True, db_comment='服务名称')
    service_desc = models.TextField(blank=True, null=True, db_comment='服务简介')
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='使用单价：元/次')
    service_url = models.TextField(blank=True, null=True, db_comment='管理服务器地址')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    state = models.IntegerField(blank=True, null=True, db_comment='管理服务器状态，0表示离线，1表示在线，2表示停用')

    class Meta:
        managed = False
        db_table = 'tb_service_type'


class TbTaskOrder(models.Model):
    order_id = models.AutoField(primary_key=True, db_comment='任务自增id')
    type_no = models.IntegerField(blank=True, null=True, db_comment='任务类型编号')
    link_id = models.CharField(max_length=16, blank=True, null=True, db_comment='下级扩展任务id，当state为3时有值')
    desc_text = models.TextField(blank=True, null=True, db_comment='文字要求')
    desc_appendix = models.TextField(blank=True, null=True, db_comment='输入附件，file_id，多个附件以|分开')
    applyer = models.CharField(max_length=255, blank=True, null=True, db_comment='申请者')
    apply_time = models.DateTimeField(blank=True, null=True, db_comment='申请时间')
    spend_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='本次花费金额')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    performer = models.IntegerField(blank=True, null=True, db_comment='分配执行者')
    allocate_time = models.DateTimeField(blank=True, null=True, db_comment='分配时间')
    finish_time = models.DateTimeField(blank=True, null=True, db_comment='结束时间')
    state = models.IntegerField(blank=True, null=True, db_comment='执行状态，0为未执行，1为正在执行，2为执行完成，3为执行失败')

    class Meta:
        managed = False
        db_table = 'tb_task_order'
        db_table_comment = '任务订单'


class TbTaskProcess(models.Model):
    process_id = models.AutoField(primary_key=True, db_comment='流程自增id')
    performer = models.IntegerField(blank=True, null=True, db_comment='执行者')
    order_id = models.IntegerField(blank=True, null=True, db_comment='关联订单id')
    start_time = models.DateTimeField(blank=True, null=True, db_comment='开始执行时间/接单时间')
    end_time = models.DateTimeField(blank=True, null=True, db_comment='结束时间')
    result = models.TextField(blank=True, null=True, db_comment='执行结果')
    appendix = models.TextField(blank=True, null=True, db_comment='结果附件，一般为file_id，若多个以|分割')
    state = models.CharField(max_length=255, blank=True, null=True, db_comment='执行状态，1为执行成功，2为执行失败')

    class Meta:
        managed = False
        db_table = 'tb_task_process'
        db_table_comment = '任务执行进度'


class TmAccount(models.Model):
    account_id = models.CharField(primary_key=True, max_length=255, db_comment='账户id')
    account_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='账户余额')
    lock_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='锁定金额')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    update_time = models.DateTimeField(blank=True, null=True, db_comment='更新时间')
    state = models.IntegerField(blank=True, null=True, db_comment='账户状态，0为未启用，1为启用，2为冻结，3为封禁')

    class Meta:
        managed = False
        db_table = 'tm_account'


class TmAccountLog(models.Model):
    order_effect_ret = models.IntegerField(blank=True, null=True, db_comment='是否是订单影响，0否，1是')
    order_id = models.IntegerField(blank=True, null=True, db_comment='关联订单编号，order_effect_ret为否是为空')
    reason = models.CharField(max_length=255, blank=True, null=True, db_comment='金额变动发生原因')
    account_id = models.CharField(max_length=255, db_comment='影响的账户id')
    effect = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='金额影响')
    before = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='变动之前的金额')
    after = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='变动之后的金额')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')

    class Meta:
        managed = False
        db_table = 'tm_account_log'


class TmLicense(models.Model):
    license_code = models.CharField(unique=True, max_length=255, blank=True, null=True, db_comment='授权码')
    save_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='价值：元')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    use_time = models.DateTimeField(blank=True, null=True, db_comment='使用时间')
    state = models.IntegerField(blank=True, null=True, db_comment='当前状态，0为未开启，1为待用，2为已使用，3为删除')

    class Meta:
        managed = False
        db_table = 'tm_license'


class TpUser(models.Model):
    user_id = models.AutoField(primary_key=True, db_comment='自增id')
    user_type = models.IntegerField(blank=True, null=True, db_comment='用户类型，0为服务商，1为客户')
    username = models.CharField(unique=True, max_length=255, blank=True, null=True, db_comment='用户名')
    secret = models.CharField(max_length=255, blank=True, null=True, db_comment='授权码')
    password = models.CharField(max_length=255, blank=True, null=True, db_comment='密码')
    all_done = models.IntegerField(blank=True, null=True, db_comment='总处理单量，只有服务商会有相关参数')
    success_done = models.IntegerField(blank=True, null=True, db_comment='完成单')
    bad_done = models.IntegerField(blank=True, null=True, db_comment='失败单')
    account_id = models.CharField(max_length=255, blank=True, null=True, db_comment='账户编码')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    state = models.IntegerField(blank=True, null=True, db_comment='当前状态，0为未启用，1为正常使用，2为封禁')

    class Meta:
        managed = False
        db_table = 'tp_user'


class TpUserLog(models.Model):
    user_id = models.IntegerField(blank=True, null=True, db_comment='服务商用户编号')
    cmd = models.IntegerField(blank=True, null=True, db_comment='行动代码')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')

    class Meta:
        managed = False
        db_table = 'tp_user_log'
