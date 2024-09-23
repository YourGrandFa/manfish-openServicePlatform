# coding: utf-8
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(150, 'utf8mb4_general_ci'), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    password = Column(String(128, 'utf8mb4_general_ci'), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150, 'utf8mb4_general_ci'), nullable=False, unique=True)
    first_name = Column(String(150, 'utf8mb4_general_ci'), nullable=False)
    last_name = Column(String(150, 'utf8mb4_general_ci'), nullable=False)
    email = Column(String(254, 'utf8mb4_general_ci'), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    app_label = Column(String(100, 'utf8mb4_general_ci'), nullable=False)
    model = Column(String(100, 'utf8mb4_general_ci'), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(BigInteger, primary_key=True)
    app = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    name = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40, 'utf8mb4_general_ci'), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False, index=True)


class TbDict(Base):
    __tablename__ = 'tb_dict'

    id = Column(Integer, primary_key=True, comment='自增id')
    dict_type = Column(VARCHAR(255), comment='服务器或区域、其他描述')
    dict_id = Column(VARCHAR(255), comment='字典id、名称、代指词')
    dict_value = Column(VARCHAR(255), comment='目标值')
    create_time = Column(DateTime, comment='创建时间')


class TbFilePermission(Base):
    __tablename__ = 'tb_file_permission'

    id = Column(Integer, primary_key=True, comment='自增id')
    file_id = Column(String(255, 'utf8mb4_general_ci'), comment='文件编号')
    user_id = Column(Integer, comment='用户编号')
    create_time = Column(DateTime, comment='创建时间')


class TbFileSave(Base):
    __tablename__ = 'tb_file_save'

    file_id = Column(String(255, 'utf8mb4_general_ci'), primary_key=True, comment='文件id')
    file_belong = Column(Integer, comment='文件归属者user_id')
    file_name = Column(String(255, 'utf8mb4_general_ci'), comment='文件名称')
    local_save_path = Column(Text(collation='utf8mb4_general_ci'), comment='本地存储地址')
    oss_path = Column(Text(collation='utf8mb4_general_ci'), comment='阿里云oss存储地址')
    create_time = Column(DateTime, comment='创建时间')
    state = Column(Integer, comment='当前状态，0为禁止访问，1为允许访问')


class TbServiceDetail(Base):
    __tablename__ = 'tb_service_detail'
    __table_args__ = {'comment': '服务资源清单'}

    service_id = Column(Integer, primary_key=True, comment='服务id')
    user_id = Column(Integer, comment='服务者/执行者user_id')
    type_no = Column(Integer, comment='任务类型编号')
    online_state = Column(Integer, comment='服务上线状态，0离线，1在线')
    state = Column(Integer, comment='服务状态，0未部署，1已部署，2已下架，3已清除，4正在维护')


class TbServiceType(Base):
    __tablename__ = 'tb_service_type'

    type_no = Column(Integer, primary_key=True, comment='服务编号')
    service_name = Column(String(255, 'utf8mb4_general_ci'), comment='服务名称')
    service_desc = Column(Text(collation='utf8mb4_general_ci'), comment='服务简介')
    price = Column(DECIMAL(8, 2), comment='使用单价：元/次')
    service_url = Column(Text(collation='utf8mb4_general_ci'), comment='管理服务器地址')
    create_time = Column(DateTime, comment='创建时间')
    state = Column(Integer, comment='管理服务器状态，0表示离线，1表示在线，2表示停用')


class TbTaskOrder(Base):
    __tablename__ = 'tb_task_order'
    __table_args__ = {'comment': '任务订单'}

    order_id = Column(Integer, primary_key=True, comment='任务自增id')
    type_no = Column(Integer, comment='任务类型编号')
    link_id = Column(VARCHAR(16), comment='下级扩展任务id，当state为3时有值')
    desc_text = Column(Text(collation='utf8mb4_general_ci'), comment='文字要求')
    desc_appendix = Column(Text(collation='utf8mb4_general_ci'), comment='输入附件，file_id，多个附件以|分开')
    applyer = Column(String(255, 'utf8mb4_general_ci'), comment='申请者')
    apply_time = Column(DateTime, comment='申请时间')
    spend_money = Column(DECIMAL(8, 2), comment='本次花费金额')
    create_time = Column(DateTime, comment='创建时间')
    performer = Column(Integer, comment='分配执行者')
    allocate_time = Column(DateTime, comment='分配时间')
    finish_time = Column(DateTime, comment='结束时间')
    state = Column(Integer, comment='执行状态，0为未执行，1为正在执行，2为执行完成，3为执行失败')


class TbTaskProces(Base):
    __tablename__ = 'tb_task_process'
    __table_args__ = {'comment': '任务执行进度'}

    process_id = Column(Integer, primary_key=True, comment='流程自增id')
    performer = Column(Integer, comment='执行者')
    order_id = Column(Integer, comment='关联订单id')
    start_time = Column(DateTime, comment='开始执行时间/接单时间')
    end_time = Column(DateTime, comment='结束时间')
    result = Column(TEXT, comment='执行结果')
    appendix = Column(TEXT, comment='结果附件，一般为file_id，若多个以|分割')
    state = Column(VARCHAR(255), comment='执行状态，1为执行成功，2为执行失败')


class TmAccount(Base):
    __tablename__ = 'tm_account'

    account_id = Column(String(255, 'utf8mb4_general_ci'), primary_key=True, comment='账户id')
    account_money = Column(DECIMAL(8, 2), comment='账户余额')
    lock_money = Column(DECIMAL(8, 2), comment='锁定金额')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')
    state = Column(Integer, comment='账户状态，0为未启用，1为启用，2为冻结，3为封禁')


class TmAccountLog(Base):
    __tablename__ = 'tm_account_log'

    id = Column(Integer, primary_key=True, comment='自增id')
    order_effect_ret = Column(Integer, comment='是否是订单影响，0否，1是')
    order_id = Column(Integer, comment='关联订单编号，order_effect_ret为否是为空')
    reason = Column(String(255, 'utf8mb4_general_ci'), comment='金额变动发生原因')
    account_id = Column(VARCHAR(255), nullable=False, comment='影响的账户id')
    effect = Column(DECIMAL(8, 2), comment='金额影响')
    before = Column(DECIMAL(8, 2), comment='变动之前的金额')
    after = Column(DECIMAL(8, 2), comment='变动之后的金额')
    create_time = Column(DateTime, comment='创建时间')


class TmLicense(Base):
    __tablename__ = 'tm_license'

    id = Column(Integer, primary_key=True, comment='自增id')
    license_code = Column(String(255, 'utf8mb4_general_ci'), unique=True, comment='授权码')
    save_money = Column(DECIMAL(8, 2), comment='价值：元')
    create_time = Column(DateTime, comment='创建时间')
    use_time = Column(DateTime, comment='使用时间')
    state = Column(Integer, comment='当前状态，0为未开启，1为待用，2为已使用，3为删除')


class TpUser(Base):
    __tablename__ = 'tp_user'

    user_id = Column(Integer, primary_key=True, comment='自增id')
    user_type = Column(Integer, comment='用户类型，0为服务商，1为客户')
    username = Column(VARCHAR(255), unique=True, comment='用户名')
    secret = Column(String(255, 'utf8mb4_general_ci'), comment='授权码')
    password = Column(VARCHAR(255), comment='密码')
    all_done = Column(Integer, comment='总处理单量，只有服务商会有相关参数')
    success_done = Column(Integer, comment='完成单')
    bad_done = Column(Integer, comment='失败单')
    account_id = Column(String(255, 'utf8mb4_general_ci'), comment='账户编码')
    create_time = Column(DateTime, comment='创建时间')
    state = Column(Integer, comment='当前状态，0为未启用，1为正常使用，2为封禁')


class TpUserLog(Base):
    __tablename__ = 'tp_user_log'

    id = Column(Integer, primary_key=True, comment='自增id')
    user_id = Column(Integer, comment='服务商用户编号')
    cmd = Column(Integer, comment='行动代码')
    create_time = Column(DateTime, comment='创建时间')


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False)
    codename = Column(String(100, 'utf8mb4_general_ci'), nullable=False)

    content_type = relationship('DjangoContentType')


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthUser')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthUser')
