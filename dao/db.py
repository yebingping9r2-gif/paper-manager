import psycopg2
from psycopg2.extras import RealDictCursor
from config.db_config import DB_CONFIG
from config.logger import logger
from utils.exceptions import DatabaseError

def get_db_connection():
    """获取数据库连接，用完记得关闭"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise DatabaseError(f"连接失败: {str(e)}")

def execute_query(sql: str, params: tuple = None, fetch: bool = True, commit: bool = False):
    """
    通用SQL执行函数
    :param sql: SQL语句，支持%s占位符
    :param params: 参数元组
    :param fetch: 是否需要返回结果
    :param commit: 是否提交事务（INSERT/UPDATE/DELETE必须设为True）
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params)

        # 写操作必须提交事务
        if commit:
            conn.commit()

        if fetch:
            result = cursor.fetchall()
            return [dict(row) for row in result]
        else:
            return cursor.rowcount

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"SQL执行失败: {sql}, 参数: {params}, 错误: {str(e)}")
        raise DatabaseError(str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

