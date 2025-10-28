from pydantic import BaseModel, Field
from typing import List, Any


class ChatRequest(BaseModel):
    query: str = Field(..., description="User's natural language question.")


class RetrievedChunk(BaseModel):
    id: str
    score: float
    text: str
    meta: Any


class ChatResponse(BaseModel):
    answer: str
    retrieved_context_preview: List[RetrievedChunk]
