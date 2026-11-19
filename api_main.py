# api_main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config.logger import logger
from utils.exceptions import PaperManagerError
from fastapi.middleware.cors import CORSMiddleware
from utils.response import error_response
from routers.ai import router as ai_router
# 导入路由模块
from routers.paper import router as paper_router

# 创建 FastAPI 应用
app = FastAPI(
    title="论文管理API",
    description="阶段A项目FastAPI版本 - 模块化结构"
)
# ========== 新增：CORS 跨域配置 ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有来源，开发阶段用；上线改成具体域名
    allow_credentials=True,    # 允许携带 Cookie
    allow_methods=["*"],       # 允许所有请求方法 GET/POST/PUT/DELETE 等
    allow_headers=["*"],       # 允许所有请求头
)
# 注册路由模块
app.include_router(paper_router)
app.include_router(ai_router)
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
        content=error_response(message=exc.message, code=400)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_main:app", host="0.0.0.0", port=8000, reload=True)
