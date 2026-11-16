from dao.paper_dao import add_paper, get_paper_by_id, list_papers, update_paper, delete_paper
from utils.exceptions import PaperNotFoundError

if __name__ == "__main__":
    print("===== 开始测试 DAO 层 =====")

    # 1. 测试新增论文
    print("\n1. 测试新增论文")
    paper_id = add_paper(
        title="大模型RAG技术研究",
        author="张三",
        publish_year=2026,
        abstract="本文研究RAG的检索优化方法"
    )
    print(f"✅ 新增成功，论文ID: {paper_id}")

    # 2. 测试根据ID查询
    print("\n2. 测试ID查询")
    paper = get_paper_by_id(paper_id)
    print(f"✅ 查询结果: 标题={paper['title']}, 作者={paper['author']}")

    # 3. 测试查询列表
    print("\n3. 测试论文列表")
    all_papers = list_papers()
    print(f"✅ 论文总数: {len(all_papers)}")

    # 关键词搜索测试
    search_result = list_papers(keyword="RAG")
    print(f"✅ 关键词'RAG'搜索结果数: {len(search_result)}")

    # 4. 测试更新
    print("\n4. 测试更新论文")
    update_paper(paper_id, title="RAG检索优化技术研究", publish_year=2025)
    updated_paper = get_paper_by_id(paper_id)
    print(f"✅ 更新后标题: {updated_paper['title']}, 年份: {updated_paper['publish_year']}")

    # 5. 测试删除
    print("\n5. 测试删除论文")
    delete_paper(paper_id)
    print(f"✅ 删除论文ID: {paper_id}")

    # 验证删除后查询应抛出异常
    try:
        get_paper_by_id(paper_id)
        print("❌ 删除失败，还能查到数据")
    except PaperNotFoundError:
        print("✅ 删除后查询正常抛出异常，验证通过")

    print("\n===== 全部测试通过 =====")
