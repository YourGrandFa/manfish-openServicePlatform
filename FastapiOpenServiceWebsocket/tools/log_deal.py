# coding:utf-8
import logging
from logging import handlers


def get_logger(log_file_path, level=logging.DEBUG, when='W0', back_count=0):
    """
    :brief  日志记录
    :param log_root: 日志存储目录
    :param log_filename: 日志名称
    :param level: 日志等级
    :param when: 间隔时间:
        S:秒
        M:分
        H:小时
        D:天
        W:每星期（interval==0时代表星期一）
        midnight: 每天凌晨
    :param back_count: 备份文件的个数，若超过该值，就会自动删除
    :return: logger
    """
    # 创建一个日志器。提供了应用程序接口
    logger = logging.getLogger()
    # 设置日志输出的最低等级,低于当前等级则会被忽略
    logger.setLevel(level)
    # 采用添加的方式进行日志写入,以防止先前日志覆盖
    logger.filemode = 'a'

    # 创建格式器
    # 这个描述的太具体了,所以没采用,示例:
    # 2024-01-24 09:33:56,877 - F:\pythonProject\log_tests\logging_both.py[line:67] - DEBUG: go
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # 增加输出到文件的配置,配置备份手段
    fh = logging.handlers.TimedRotatingFileHandler(
        filename=log_file_path,
        when=when,
        backupCount=back_count,
        encoding='utf-8')
    fh.setLevel(level)

    # 设置日志输出格式
    fh.setFormatter(formatter)

    # 将处理器，添加至日志器中
    logger.addHandler(fh)

    return logger
