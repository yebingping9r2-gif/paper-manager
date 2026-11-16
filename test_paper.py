from utils.exceptions import PaperNotFoundError, DatabaseError

# 测试论文不存在异常
try:
    raise PaperNotFoundError(paper_id=1)
except PaperNotFoundError as e:
    print(f"捕获到业务异常: {e.message}")

# 测试数据库异常
try:
    raise DatabaseError("连接超时")
except DatabaseError as e:
    print(f"捕获到数据库异常: {e.message}")
