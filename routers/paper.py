# routers/paper.py
from fastapi import APIRouter, Depends
from dao.paper_dao import add_paper, get_paper_by_id, list_papers, update_paper, delete_paper
from schemas.paper import PaperCreate, PaperUpdate
from utils.response import success_response
from dao.db import get_db
# 创建路由实例
# prefix: 给该模块所有接口统一加前缀，不用每个都写 /papers
# tags:  Swagger 文档里的分组名称
router = APIRouter(
    prefix="/papers",
    tags=["论文管理"]
)

# 1. 查询论文列表（支持关键词搜索）
@router.get("", summary="查询论文列表")
def get_paper_list(keyword: str | None = None, conn = Depends(get_db)):
    papers = list_papers(conn,keyword)
    return success_response(data=papers, message="查询成功")
    #return {"code": 200, "message": "查询成功", "data": papers}

# 2. 根据ID查询单篇论文
@router.get("/{paper_id}", summary="根据ID查询论文")
def get_paper(paper_id: int, conn = Depends(get_db)):
    paper = get_paper_by_id(conn,paper_id)
    return success_response(data=paper, message="查询成功")

# 3. 新增论文
@router.post("", summary="新增论文")
def create_paper(paper: PaperCreate, conn = Depends(get_db)):
    paper_id = add_paper(
        conn,
        title=paper.title,
        author=paper.author,
        publish_year=paper.publish_year,
        abstract=paper.abstract
    )
    return success_response(data={"id": paper_id}, message="新增成功")

# 4. 更新论文
@router.put("/{paper_id}", summary="更新论文")
def modify_paper(paper_id: int, paper: PaperUpdate, conn = Depends(get_db)):
    update_paper(
        conn,
        paper_id=paper_id,
        title=paper.title,
        author=paper.author,
        publish_year=paper.publish_year,
        abstract=paper.abstract
    )
    return success_response(message="更新成功")

# 5. 删除论文
@router.delete("/{paper_id}", summary="删除论文")
def remove_paper(paper_id: int, conn = Depends(get_db)):
    delete_paper(conn,paper_id)
    return success_response(message="删除成功")
