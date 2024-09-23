import pymysql
import configparser
import random
import string
import uuid


def generate_random_string(length=16):
    # 定义字符集，包括大小写字母和数字
    characters = string.ascii_letters + string.digits
    # 从字符集中随机选择字符
    return ''.join(random.choice(characters) for _ in range(length))


CONF = configparser.ConfigParser()
CONF.read('open_service.ini')

#
insert_user = [{
    'user_type': 0,
    'applyer_name': 'manfish',
    'secret': generate_random_string(),
    'pwd': generate_random_string(length=8),
    'account_id': str(uuid.uuid4()),
    'state': 1
}]
print(generate_random_string(), generate_random_string(length=8))

MYSQL_DB = CONF['system_db']
with pymysql.connect(host=MYSQL_DB['host'], port=int(MYSQL_DB['port']), user=MYSQL_DB['user'],
                     password=MYSQL_DB['password'], database=MYSQL_DB['database']) as db:
    with db.cursor() as cursor:
        user_sql = 'insert into tp_user(user_type, applyer_name, secret, pwd, account_id, create_time, state) \
        values (%s, %s, %s, %s, %s, now(), %s)'

        account_sql = 'insert into tm_account(account_id, account_money, lock_money, create_time, state) \
                    values (%s, %s, %s, now(), 1)'

        for user in insert_user:
            cursor.execute(account_sql, (
                user['account_id'],
                0,
                0,
            ))

            cursor.execute(user_sql, (
                user['user_type'],
                user['applyer_name'],
                user['secret'],
                user['pwd'],
                user['account_id'],
                user['state'],
            ))

            db.commit()
