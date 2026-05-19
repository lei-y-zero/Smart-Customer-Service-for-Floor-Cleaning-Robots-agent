import logging
import os
from datetime import datetime
# import agent.utils.path_tool
from utils.path_tool import get_abs_path

#日志保存的根目录
LOG_ROOT=get_abs_path("logs")

#确保日志存在
os.makedirs(LOG_ROOT,exist_ok=True)
#日志格式配置
DEFAULT_LOGGING_FORMAT=logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
)

def get_loger(
        name:str = "agent",
        console_level:int =logging.INFO,
        file_level:int=logging.DEBUG,
        log_file=None,
)->logging.Logger:
    logger=logging.Logger(name)
    logger.setLevel(logging.DEBUG)

    #避免重复获取日志
    if logger.handlers:
        return logger
    #控制台handler
    console_handeler=logging.StreamHandler()
    console_handeler.setLevel(console_level)
    console_handeler.setFormatter(DEFAULT_LOGGING_FORMAT)

    logger.addHandler(console_handeler)

    #文件handler
    if not log_file:       #日志文件存放路径
        log_file=os.path.join(LOG_ROOT,f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler=logging.FileHandler(log_file,encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOGGING_FORMAT)

    logger.addHandler(file_handler)
    return logger

#快捷获取日志器
logger=get_loger()

if __name__=='__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")
