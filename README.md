# 论文管理 CLI 工具
阶段A工程化练习项目，基于 Python + PostgreSQL 实现的命令行论文管理系统。

## 技术栈
- Python 3.x
- PostgreSQL
- psycopg2-binary

## 功能
1. 新增论文
2. 按ID查询论文
3. 关键词搜索论文
4. 更新论文信息
5. 删除论文

## 运行步骤
1. 安装依赖：`pip install -r requirements.txt`
2. 在PostgreSQL中执行建表SQL（见docs）
3. 修改 config/db_config.py 中的数据库密码
4. 运行：`python main.py`

## 项目结构
- config/ 配置文件（日志、数据库）
- dao/ 数据库交互层
- utils/ 通用工具（异常、装饰器）
- tests/ 单元测试
