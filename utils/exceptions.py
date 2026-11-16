# 基础业务异常类
class PaperManagerError(Exception):
    """项目所有自定义异常的基类"""
    pass

# 论文不存在异常
class PaperNotFoundError(PaperManagerError):
    def __init__(self, paper_id: int = None, title: str = None):
        if paper_id:
            self.message = f"ID为 {paper_id} 的论文不存在"
        elif title:
            self.message = f"标题为「{title}」的论文不存在"
        else:
            self.message = "论文不存在"
        super().__init__(self.message)

# 数据库操作异常
class DatabaseError(PaperManagerError):
    def __init__(self, detail: str):
        self.message = f"数据库操作失败: {detail}"
        super().__init__(self.message)
