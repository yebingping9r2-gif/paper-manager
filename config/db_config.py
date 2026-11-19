DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "123456",
    "dbname": "postgres"
}
import os

# 文件上传存储目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# 确保目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)
