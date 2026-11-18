# routers/paper.py
from fastapi import APIRouter
from dao.paper_dao import add_paper, get_paper_by_id, list_papers, update_paper, delete_paper
from schemas.paper import PaperCreate, PaperUpdate

# 创建路由实例
# prefix: 给该模块所有接口统一加前缀，不用每个都写 /papers
# tags:  Swagger 文档里的分组名称
router = APIRouter(
    prefix="/papers",
    tags=["论文管理"]
)

# 1. 查询论文列表（支持关键词搜索）
@router.get("", summary="查询论文列表")
def get_paper_list(keyword: str | None = None):
    papers = list_papers(keyword)
    return {"code": 200, "message": "查询成功", "data": papers}

# 2. 根据ID查询单篇论文
@router.get("/{paper_id}", summary="根据ID查询论文")
def get_paper(paper_id: int):
    paper = get_paper_by_id(paper_id)
    return {"code": 200, "message": "查询成功", "data": paper}

# 3. 新增论文
@router.post("", summary="新增论文")
def create_paper(paper: PaperCreate):
    paper_id = add_paper(
        title=paper.title,
        author=paper.author,
        publish_year=paper.publish_year,
        abstract=paper.abstract
    )
    return {"code": 200, "message": "新增成功", "data": {"id": paper_id}}

# 4. 更新论文
@router.put("/{paper_id}", summary="更新论文")
def modify_paper(paper_id: int, paper: PaperUpdate):
    update_paper(
        paper_id=paper_id,
        title=paper.title,
        author=paper.author,
        publish_year=paper.publish_year,
        abstract=paper.abstract
    )
    return {"code": 200, "message": "更新成功"}

# 5. 删除论文
@router.delete("/{paper_id}", summary="删除论文")
def remove_paper(paper_id: int):
    delete_paper(paper_id)
    return {"code": 200, "message": "删除成功"}
