from dao.paper_dao import add_paper, get_paper_by_id, list_papers, update_paper, delete_paper
from config.logger import logger
from utils.exceptions import PaperManagerError
from utils.decorators import time_it

def print_menu():
    print("\n===== 论文管理系统 =====")
    print("1. 新增论文")
    print("2. 根据ID查询论文")
    print("3. 查询所有论文/关键词搜索")
    print("4. 更新论文信息")
    print("5. 删除论文")
    print("0. 退出")
    print("========================")

@time_it
def main():
    logger.info("论文管理系统启动")
    while True:
        print_menu()
        choice = input("请输入选项: ").strip()
        
        try:
            if choice == "1":
                title = input("请输入论文标题: ").strip()
                author = input("请输入作者(可空): ").strip() or None
                year_str = input("请输入发表年份(可空): ").strip()
                publish_year = int(year_str) if year_str else None
                abstract = input("请输入摘要(可空): ").strip() or None
                
                paper_id = add_paper(title, author, publish_year, abstract)
                print(f"✅ 新增成功，论文ID: {paper_id}")

            elif choice == "2":
                pid = int(input("请输入论文ID: "))
                paper = get_paper_by_id(pid)
                print("\n论文详情:")
                for k, v in paper.items():
                    print(f"  {k}: {v}")

            elif choice == "3":
                keyword = input("输入关键词搜索(直接回车查全部): ").strip() or None
                papers = list_papers(keyword)
                print(f"\n共找到 {len(papers)} 篇论文:")
                for p in papers:
                    print(f"  [{p['id']}] {p['title']} - {p['author']} ({p['publish_year']})")

            elif choice == "4":
                pid = int(input("请输入要修改的论文ID: "))
                # 先查询确认存在
                get_paper_by_id(pid)
                print("直接回车表示不修改该字段")
                title = input("新标题: ").strip() or None
                author = input("新作者: ").strip() or None
                year_str = input("新年份: ").strip()
                publish_year = int(year_str) if year_str else None
                abstract = input("新摘要: ").strip() or None
                
                update_paper(pid, title, author, publish_year, abstract)
                print("✅ 更新成功")

            elif choice == "5":
                pid = int(input("请输入要删除的论文ID: "))
                confirm = input(f"确认删除ID为{pid}的论文吗？(y/n): ").strip().lower()
                if confirm == 'y':
                    delete_paper(pid)
                    print("✅ 删除成功")
                else:
                    print("已取消删除")

            elif choice == "0":
                logger.info("系统退出")
                print("再见！")
                break

            else:
                print("❌ 无效选项，请重新输入")

        except PaperManagerError as e:
            print(f"❌ 业务错误: {e.message}")
            logger.warning(f"业务异常: {e.message}")
        except ValueError:
            print("❌ 输入格式错误，请输入数字")
        except Exception as e:
            print(f"❌ 系统错误: {str(e)}")
            logger.error(f"未捕获异常: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()

