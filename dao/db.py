import psycopg2
from psycopg2.extras import RealDictCursor
from config.db_config import DB_CONFIG
from config.logger import logger
from utils.exceptions import DatabaseError
from fastapi import Depends
from typing import Generator
def get_db_connection():
    """获取数据库连接，用完记得关闭"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise DatabaseError(f"连接失败: {str(e)}")

def execute_query(conn, sql: str, params: tuple = None, fetch: bool = True):
    """
    通用SQL执行工具（接收外部传入的连接）
    :param conn: 外部注入的数据库连接
    """
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params)
        
        if fetch:
            result = cursor.fetchall()
            return [dict(row) for row in result]
        else:
            conn.commit()
            return cursor.rowcount
            
    except Exception as e:
        conn.rollback()
        logger.error(f"SQL执行失败: {sql}, 参数: {params}, 错误: {str(e)}")
        raise DatabaseError(str(e))
    finally:
        if cursor:
            cursor.close()
# ========== 新增：数据库连接依赖项 ==========
def get_db() -> Generator:
    """
    依赖函数：为每个请求创建一个数据库连接
    请求结束后自动关闭连接
    - `yield` 前面的代码：**请求进来时执行**，创建数据库连接
- `yield conn`：把连接对象传给使用这个依赖的接口函数
- `yield` 后面的代码（finally 里的）：**请求结束后执行**，自动关闭连接，释放资源
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn  # 把连接交给接口函数使用
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise DatabaseError(f"连接失败: {str(e)}")
    finally:
        if conn:
            conn.close()
            logger.debug("数据库连接已关闭")