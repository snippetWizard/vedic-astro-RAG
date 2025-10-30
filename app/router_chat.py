from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, List
from .rag_pipeline import run_rag
from .schemas import RetrievedChunk


# ----------------------------------------------------
# 🧩 Router setup
# ----------------------------------------------------
router = APIRouter(prefix="/chat", tags=["chat"])


# ----------------------------------------------------
# 📥 Request / 📤 Response Models
# ----------------------------------------------------
class ChatRequest(BaseModel):
    query: str = Field(..., description="User's natural language question or prompt.")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Final model-generated response to the query.")
    retrieved_context_preview: List[RetrievedChunk] = Field(
        ..., description="List of retrieved chunks used to answer the query."
    )


# ----------------------------------------------------
# ⚙️ Core Endpoint
# ----------------------------------------------------
@router.post("/rag", response_model=ChatResponse)
async def rag_chat_endpoint(body: ChatRequest) -> Any:
    """
    🔮 Retrieval-Augmented Chat Endpoint

    This endpoint performs:
      1️⃣ Embedding-based retrieval from ChromaDB
      2️⃣ Context assembly for the top-k results
      3️⃣ GPT-5 reasoning via OpenAI API using the context
      4️⃣ Returns final answer + preview of retrieved chunks

    Example Request:
    {
      "query": "What happens if the Sun is in the first house?"
    }

    Example Response:
    {
      "answer": "...",
      "retrieved_context_preview": [
        {
          "id": "uuid",
          "score": 0.92,
          "text": "Planet Sun in the 1st House ...",
          "meta": { "type": "planet_in_house", "house_number": 1, "planet_name": "Sun" }
        }
      ]
    }
    """

    try:
        llm_answer, retrieved = await run_rag(body.query)

        if not llm_answer:
            raise HTTPException(status_code=404, detail="No relevant information found.")

        return ChatResponse(
            answer=llm_answer,
            retrieved_context_preview=retrieved
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {str(e)}")
