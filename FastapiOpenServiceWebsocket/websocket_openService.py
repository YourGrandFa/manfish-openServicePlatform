import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from tools import log_deal, variables, dependencies
import logging
from fastapi.responses import JSONResponse
from routers import ws, file

config_path = 'open_service.ini'
# 解析配置文件
CONF = variables.set_conf(config_path)
# 设置阿里云OSS服务
variables.set_oss()

# 定义API的访问端口
API_PORT = CONF['global']['api_port']

FILE_HOME = CONF['file_path_windows']
API_LOG_PATH = os.path.join(FILE_HOME['file_home'], FILE_HOME['api_log'])


if __name__ == "__main__":
    import uvicorn

    # 创建一个日志器。提供控制台和日志输出
    LOGGER = log_deal.get_logger(API_LOG_PATH, level=logging.DEBUG, when='W0', back_count=0)

    # 配置数据库连接池
    SYSTEM_DB = CONF['system_db']
    dependencies.create_SessionLocal(SYSTEM_DB)

    app = FastAPI(docs_url=None, debug=True)

    # 增加防跨域组件
    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        back = {"status": False, "msg": exc.errors(), "data": exc.body}
        print(back)
        return JSONResponse(
            status_code=422,
            content=back,
        )

    app.include_router(ws.router)
    app.include_router(file.router)

    # 定义API的访问端口
    API_PORT = CONF['global']['api_port']

    uvicorn.run(app, host="0.0.0.0", port=int(API_PORT))
