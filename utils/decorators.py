import time
from functools import wraps
from config.logger import logger

def time_it(func):
    """计时装饰器：统计函数执行耗时并打日志"""
    @wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        cost = time.time() - start
        logger.info(f"函数 {func.__name__} 执行完成，耗时: {cost:.4f} 秒")
        return result
    return wrapper
