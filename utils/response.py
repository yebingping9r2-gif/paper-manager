# utils/response.py
from typing import Any

def success_response(data: Any = None, message: str = "操作成功") -> dict:
    """统一成功响应格式"""
    return {
        "code": 200,
        "message": message,
        "data": data
    }

def error_response(message: str = "操作失败", code: int = 400, data: Any = None) -> dict:
    """统一错误响应格式"""
    return {
        "code": code,
        "message": message,
        "data": data
    }
