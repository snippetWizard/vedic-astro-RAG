import httpx
from typing import List
from .config import settings

# NOTE:
# We're doing manual HTTP calls so you can swap OpenAI provider later (Azure, custom proxy, etc.)
# This layer is the ONLY place in the repo that knows about OpenAI’s actual endpoints.


OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_EMBED_URL = "https://api.openai.com/v1/embeddings"


async def generate_embedding(text: str) -> List[float]:
    """
    Create an embedding vector for a given text using OpenAI embeddings.
    We'll store these vectors in Qdrant.

    text: any text chunk (house description, planet meaning, etc.)
    returns: list[float] - embedding vector
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            OPENAI_EMBED_URL,
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.openai_embedding_model,
                "input": text
            }
        )
    resp.raise_for_status()
    data = resp.json()
    return data["data"][0]["embedding"]


async def generate_answer(system_prompt: str, user_question: str, context: str) -> str:
    """
    Call the LLM (GPT-5 Thinking) with retrieved context and user query.

    We give the model:
    - system message (how to behave)
    - context block (retrieved knowledge from vector DB)
    - final user question

    We DO NOT let the model hallucinate astrology predictions outside provided context.
    We'll instruct it to cite which section of context it used logically,
    BUT we won't expose file paths to the end user.
    """
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": (
                "You are an expert Vedic Astrology assistant.\n"
                "You must answer ONLY using the provided 'CONTEXT' below.\n"
                "If the user asks for personal predictions (like marriage date, health forecast, etc.), "
                "political opinion, medical treatment, or anything not covered in CONTEXT, "
                "politely say you cannot answer.\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"USER QUESTION:\n{user_question}"
            )
        }
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            OPENAI_CHAT_URL,
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.openai_chat_model,
                "temperature": 0.4,  # calm, factual
                "max_tokens": 600,
                "messages": messages
            }
        )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
