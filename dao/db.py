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

def execute_query(conn, sql: str, params: tuple = None, fetch: bool = True, commit: bool = None):
    """
    通用SQL执行工具
    :param conn: 外部注入的数据库连接
    :param sql: SQL语句
    :param params: 参数元组
    :param fetch: 是否提取返回结果
    :param commit: 是否强制提交事务；为None时自动判断：fetch=False默认提交
    """
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params)

        # 自动判断是否需要提交
        if commit is None:
            commit = not fetch

        # 提取结果
        result = None
        if fetch:
            result = cursor.fetchall()
            result = [dict(row) for row in result]
        else:
            result = cursor.rowcount

        # 提交事务
        if commit:
            conn.commit()

        return result

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