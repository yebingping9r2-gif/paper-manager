import logging
import os
from datetime import datetime

# 日志文件保存目录
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志文件名按日期生成
log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")

# 日志格式：时间 - 日志级别 - 文件名:行号 - 日志内容
log_format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"

# 配置日志根记录器
logger = logging.getLogger("paper_manager")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# 1. 控制台输出处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format))

# 2. 文件输出处理器
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

# 把处理器添加到日志器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 对外导出，其他文件直接 from config.logger import logger 使用
if __name__ == "__main__":
    logger.info("日志配置测试成功")
    logger.debug("调试信息")
    logger.error("错误信息测试")
