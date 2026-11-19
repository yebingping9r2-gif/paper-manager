from dao.db import execute_query
from config.logger import logger
from utils.exceptions import PaperNotFoundError
from utils.decorators import time_it

@time_it
def add_paper(conn,title: str, author: str = None, publish_year: int = None, abstract: str = None) -> int:
    """新增论文，返回新插入的论文ID"""
    sql = """
        INSERT INTO papers (title, author, publish_year, abstract)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    result = execute_query(conn, sql, (title, author, publish_year, abstract), fetch=True)
    paper_id = result[0]['id']
    logger.info(f"新增论文成功，ID: {paper_id}, 标题: {title}")
    return paper_id

@time_it
def get_paper_by_id(conn,paper_id: int) -> dict:
    """根据ID查询论文"""
    sql = "SELECT * FROM papers WHERE id = %s;"
    result = execute_query(conn,sql, (paper_id,))
    if not result:
        raise PaperNotFoundError(paper_id=paper_id)
    return result[0]

@time_it
def list_papers(conn,keyword: str = None) -> list:
    """查询所有论文，支持按标题关键词模糊搜索"""
    if keyword:
        sql = "SELECT * FROM papers WHERE title LIKE %s ORDER BY id DESC;"
        params = (f"%{keyword}%",)
    else:
        sql = "SELECT * FROM papers ORDER BY id DESC;"
        params = None
    return execute_query(conn,sql, params)

def update_paper(conn,paper_id: int, title: str = None, author: str = None, 
                 publish_year: int = None, abstract: str = None) -> bool:
    """更新论文信息"""
    # 先检查论文是否存在
    get_paper_by_id(conn,paper_id)
    
    update_fields = []
    params = []
    if title is not None:
        update_fields.append("title = %s")
        params.append(title)
    if author is not None:
        update_fields.append("author = %s")
        params.append(author)
    if publish_year is not None:
        update_fields.append("publish_year = %s")
        params.append(publish_year)
    if abstract is not None:
        update_fields.append("abstract = %s")
        params.append(abstract)
    
    if not update_fields:
        return False
    
    sql = f"UPDATE papers SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s;"
    params.append(paper_id)
    
    rows = execute_query(conn,sql, tuple(params), fetch=False)
    logger.info(f"更新论文ID: {paper_id}，受影响行数: {rows}")
    return rows > 0

def delete_paper(conn,paper_id: int) -> bool:
    """删除论文"""
    get_paper_by_id(conn, paper_id)
    sql = "DELETE FROM papers WHERE id = %s;"
    rows = execute_query(conn,sql, (paper_id,), fetch=False)
    logger.info(f"删除论文ID: {paper_id}，受影响行数: {rows}")
    return rows > 0

def add_paper_with_file(conn, title: str, file_name: str, file_path: str,
                        author: str = None, publish_year: int = None, abstract: str = None):
    """
    上传PDF时新增论文，附带文件名和文件路径
    """
    sql = """
        INSERT INTO papers (title, author, publish_year, abstract, file_name, file_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    params = (title, author, publish_year, abstract, file_name, file_path)
    result = execute_query(conn, sql, params, fetch=True, commit=True)
    paper_id = result[0]['id']
    logger.info(f"上传论文成功，ID: {paper_id}, 文件名: {file_name}")
    return paper_id
