# routers/ai.py
from fastapi import APIRouter
from schemas.ai import ChatRequest
from llm.client import chat_with_llm
from utils.response import success_response

router = APIRouter(
    prefix="/ai",
    tags=["AI问答"]
)

@router.post("/chat", summary="单轮AI问答")
def chat(request: ChatRequest):
    answer = chat_with_llm(request.question)
    return success_response(data={"answer": answer}, message="回答生成成功")
