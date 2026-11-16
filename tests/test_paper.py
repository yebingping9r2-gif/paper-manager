import pytest
from dao.paper_dao import add_paper, get_paper_by_id, delete_paper
from utils.exceptions import PaperNotFoundError

def test_add_and_get_paper():
    # 新增
    pid = add_paper("测试论文", "测试作者", 2026, "测试摘要")
    assert pid > 0
    
    # 查询
    paper = get_paper_by_id(pid)
    assert paper['title'] == "测试论文"
    assert paper['author'] == "测试作者"
    
    # 清理
    delete_paper(pid)
    
    # 删除后查询应抛出异常
    with pytest.raises(PaperNotFoundError):
        get_paper_by_id(pid)
