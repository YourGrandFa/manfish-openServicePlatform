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
    dict_type = models.CharField(max_length=255, blank=True, null=True, db_comment='��������������������')
    dict_id = models.CharField(max_length=255, blank=True, null=True, db_comment='�ֵ�id�����ơ���ָ��')
    dict_value = models.CharField(max_length=255, blank=True, null=True, db_comment='Ŀ��ֵ')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')

    class Meta:
        managed = False
        db_table = 'tb_dict'


class TbFilePermission(models.Model):
    file_id = models.CharField(max_length=255, blank=True, null=True, db_comment='�ļ����')
    user_id = models.IntegerField(blank=True, null=True, db_comment='�û����')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')

    class Meta:
        managed = False
        db_table = 'tb_file_permission'


class TbFileSave(models.Model):
    file_id = models.CharField(primary_key=True, max_length=255, db_comment='�ļ�id')
    file_belong = models.IntegerField(blank=True, null=True, db_comment='�ļ�������user_id')
    file_name = models.CharField(max_length=255, blank=True, null=True, db_comment='�ļ�����')
    local_save_path = models.TextField(blank=True, null=True, db_comment='���ش洢��ַ')
    oss_path = models.TextField(blank=True, null=True, db_comment='������oss�洢��ַ')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    state = models.IntegerField(blank=True, null=True, db_comment='��ǰ״̬��0Ϊ��ֹ���ʣ�1Ϊ�������')

    class Meta:
        managed = False
        db_table = 'tb_file_save'


class TbServiceDetail(models.Model):
    service_id = models.AutoField(primary_key=True, db_comment='����id')
    user_id = models.IntegerField(blank=True, null=True, db_comment='������/ִ����user_id')
    type_no = models.IntegerField(blank=True, null=True, db_comment='�������ͱ��')
    online_state = models.IntegerField(blank=True, null=True, db_comment='��������״̬��0���ߣ�1����')
    state = models.IntegerField(blank=True, null=True, db_comment='����״̬��0δ����1�Ѳ���2���¼ܣ�3�������4����ά��')

    class Meta:
        managed = False
        db_table = 'tb_service_detail'
        db_table_comment = '������Դ�嵥'


class TbServiceType(models.Model):
    type_no = models.AutoField(primary_key=True, db_comment='������')
    service_name = models.CharField(max_length=255, blank=True, null=True, db_comment='��������')
    service_desc = models.TextField(blank=True, null=True, db_comment='������')
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='ʹ�õ��ۣ�Ԫ/��')
    service_url = models.TextField(blank=True, null=True, db_comment='�����������ַ')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    state = models.IntegerField(blank=True, null=True, db_comment='���������״̬��0��ʾ���ߣ�1��ʾ���ߣ�2��ʾͣ��')

    class Meta:
        managed = False
        db_table = 'tb_service_type'


class TbTaskOrder(models.Model):
    order_id = models.AutoField(primary_key=True, db_comment='��������id')
    type_no = models.IntegerField(blank=True, null=True, db_comment='�������ͱ��')
    link_id = models.CharField(max_length=16, blank=True, null=True, db_comment='�¼���չ����id����stateΪ3ʱ��ֵ')
    desc_text = models.TextField(blank=True, null=True, db_comment='����Ҫ��')
    desc_appendix = models.TextField(blank=True, null=True, db_comment='���븽����file_id�����������|�ֿ�')
    applyer = models.CharField(max_length=255, blank=True, null=True, db_comment='������')
    apply_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    spend_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='���λ��ѽ��')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    performer = models.IntegerField(blank=True, null=True, db_comment='����ִ����')
    allocate_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    finish_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    state = models.IntegerField(blank=True, null=True, db_comment='ִ��״̬��0Ϊδִ�У�1Ϊ����ִ�У�2Ϊִ����ɣ�3Ϊִ��ʧ��')

    class Meta:
        managed = False
        db_table = 'tb_task_order'
        db_table_comment = '���񶩵�'


class TbTaskProcess(models.Model):
    process_id = models.AutoField(primary_key=True, db_comment='��������id')
    performer = models.IntegerField(blank=True, null=True, db_comment='ִ����')
    order_id = models.IntegerField(blank=True, null=True, db_comment='��������id')
    start_time = models.DateTimeField(blank=True, null=True, db_comment='��ʼִ��ʱ��/�ӵ�ʱ��')
    end_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    result = models.TextField(blank=True, null=True, db_comment='ִ�н��')
    appendix = models.TextField(blank=True, null=True, db_comment='���������һ��Ϊfile_id���������|�ָ�')
    state = models.CharField(max_length=255, blank=True, null=True, db_comment='ִ��״̬��1Ϊִ�гɹ���2Ϊִ��ʧ��')

    class Meta:
        managed = False
        db_table = 'tb_task_process'
        db_table_comment = '����ִ�н���'


class TmAccount(models.Model):
    account_id = models.CharField(primary_key=True, max_length=255, db_comment='�˻�id')
    account_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='�˻����')
    lock_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='�������')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    update_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    state = models.IntegerField(blank=True, null=True, db_comment='�˻�״̬��0Ϊδ���ã�1Ϊ���ã�2Ϊ���ᣬ3Ϊ���')

    class Meta:
        managed = False
        db_table = 'tm_account'


class TmAccountLog(models.Model):
    order_effect_ret = models.IntegerField(blank=True, null=True, db_comment='�Ƿ��Ƕ���Ӱ�죬0��1��')
    order_id = models.IntegerField(blank=True, null=True, db_comment='����������ţ�order_effect_retΪ����Ϊ��')
    reason = models.CharField(max_length=255, blank=True, null=True, db_comment='���䶯����ԭ��')
    account_id = models.CharField(max_length=255, db_comment='Ӱ����˻�id')
    effect = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='���Ӱ��')
    before = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='�䶯֮ǰ�Ľ��')
    after = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='�䶯֮��Ľ��')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')

    class Meta:
        managed = False
        db_table = 'tm_account_log'


class TmLicense(models.Model):
    license_code = models.CharField(unique=True, max_length=255, blank=True, null=True, db_comment='��Ȩ��')
    save_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, db_comment='��ֵ��Ԫ')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    use_time = models.DateTimeField(blank=True, null=True, db_comment='ʹ��ʱ��')
    state = models.IntegerField(blank=True, null=True, db_comment='��ǰ״̬��0Ϊδ������1Ϊ���ã�2Ϊ��ʹ�ã�3Ϊɾ��')

    class Meta:
        managed = False
        db_table = 'tm_license'


class TpUser(models.Model):
    user_id = models.AutoField(primary_key=True, db_comment='����id')
    user_type = models.IntegerField(blank=True, null=True, db_comment='�û����ͣ�0Ϊ�����̣�1Ϊ�ͻ�')
    username = models.CharField(unique=True, max_length=255, blank=True, null=True, db_comment='�û���')
    secret = models.CharField(max_length=255, blank=True, null=True, db_comment='��Ȩ��')
    password = models.CharField(max_length=255, blank=True, null=True, db_comment='����')
    all_done = models.IntegerField(blank=True, null=True, db_comment='�ܴ�������ֻ�з����̻�����ز���')
    success_done = models.IntegerField(blank=True, null=True, db_comment='��ɵ�')
    bad_done = models.IntegerField(blank=True, null=True, db_comment='ʧ�ܵ�')
    account_id = models.CharField(max_length=255, blank=True, null=True, db_comment='�˻�����')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')
    state = models.IntegerField(blank=True, null=True, db_comment='��ǰ״̬��0Ϊδ���ã�1Ϊ����ʹ�ã�2Ϊ���')

    class Meta:
        managed = False
        db_table = 'tp_user'


class TpUserLog(models.Model):
    user_id = models.IntegerField(blank=True, null=True, db_comment='�������û����')
    cmd = models.IntegerField(blank=True, null=True, db_comment='�ж�����')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='����ʱ��')

    class Meta:
        managed = False
        db_table = 'tp_user_log'
