from dao.db import execute_query
result = execute_query("SELECT 1 as test_num")
print(result)
