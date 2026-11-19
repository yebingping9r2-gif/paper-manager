# routers/paper.py
from fastapi import APIRouter, Depends
from dao.paper_dao import add_paper, get_paper_by_id, list_papers, update_paper, delete_paper
from schemas.paper import PaperCreate, PaperUpdate
from utils.response import success_response
from dao.db import get_db
from fastapi import UploadFile, File, Form
import os
import uuid
from config.db_config import UPLOAD_DIR
from dao.paper_dao import add_paper_with_file

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

# 6. 上传PDF论文
@router.post("/upload", summary="上传PDF论文")
def upload_paper(
    file: UploadFile = File(..., description="PDF论文文件"),
    title: str = Form(None, description="论文标题，不传则用文件名"),
    conn = Depends(get_db)
):
    # 1. 校验文件格式，只允许PDF
    if not file.filename.lower().endswith(".pdf"):
        return error_response(message="只支持上传PDF文件", code=400)

    # 2. 生成唯一文件名，防止重名覆盖
    file_ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)

    # 3. 保存文件到本地
    try:
        with open(save_path, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        logger.error(f"文件保存失败: {str(e)}")
        return error_response(message="文件保存失败", code=500)

    # 4. 标题默认用文件名
    final_title = title if title else os.path.splitext(file.filename)[0]

    # 5. 写入数据库
    paper_id = add_paper_with_file(
        conn,
        title=final_title,
        file_name=file.filename,
        file_path=save_path
    )

    return success_response(
        data={"id": paper_id, "title": final_title, "file_name": file.filename},
        message="上传成功"
    )
