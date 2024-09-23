from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SessionLocal = None


# 创建数据池
def create_SessionLocal(SYSTEM_DB):
    global SessionLocal

    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(SYSTEM_DB['user'], SYSTEM_DB['password'],
                                                                      SYSTEM_DB['host'],
                                                                      SYSTEM_DB['port'], SYSTEM_DB['database'])

    # 设置mysql数据池
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=10,  # 设置连接池大小
        max_overflow=20,  # 允许的最大连接数（包含连接池内和外）
        pool_timeout=30  # 连接池超时时间
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖项函数，返回异步数据库会话
async def get_db():
    global SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
