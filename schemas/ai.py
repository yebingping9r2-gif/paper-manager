# schemas/ai.py
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., description="用户的问题内容", min_length=1)
