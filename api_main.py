# api_main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config.logger import logger
from utils.exceptions import PaperManagerError

# 导入路由模块
from routers.paper import router as paper_router

# 创建 FastAPI 应用
app = FastAPI(
    title="论文管理API",
    description="阶段A项目FastAPI版本 - 模块化结构"
)

# 注册路由模块
app.include_router(paper_router)

# 健康检查接口
@app.get("/", summary="健康检查", tags=["系统"])
def hello():
    logger.info("收到健康检查请求")
    return {"code": 200, "message": "服务运行正常", "data": "Hello FastAPI"}

# 全局业务异常处理
@app.exception_handler(PaperManagerError)
async def paper_exception_handler(request: Request, exc: PaperManagerError):
    logger.warning(f"业务异常: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": exc.message, "data": None}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_main:app", host="0.0.0.0", port=8000, reload=True)
