import os
import httpx
from typing import List
from .config import settings

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # we can override this in .env if you're on Azure or a proxy
# Guard against missing "/v1" when pointing to api.openai.com
if "api.openai.com" in OPENAI_BASE_URL and not OPENAI_BASE_URL.rstrip("/").endswith("/v1"):
    OPENAI_BASE_URL = OPENAI_BASE_URL.rstrip("/") + "/v1"
CHAT_ENDPOINT = f"{OPENAI_BASE_URL}/chat/completions"
EMBED_ENDPOINT = f"{OPENAI_BASE_URL}/embeddings"


async def generate_embedding(text: str) -> List[float]:
    """
    Create an embedding vector for a given text using OpenAI embeddings.
    If you're on Azure OpenAI, set OPENAI_BASE_URL in .env to your Azure endpoint, e.g.:
    https://my-resource.openai.azure.com/openai/deployments/my-embedding-model
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            EMBED_ENDPOINT,
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.openai_embedding_model,
                "input": text
            }
        )

    # raise clearer error
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(
            f"OpenAI embedding call failed ({e.response.status_code}): {e.response.text}"
        )

    data = resp.json()
    return data["data"][0]["embedding"]


async def generate_answer(system_prompt: str, user_question: str, context: str) -> str:
    """
    Generate an answer from GPT-5 Thinking (or your chosen chat model)
    using the standard /v1/chat/completions route.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "You are an expert Vedic Astrology assistant.\n"
                "Answer ONLY using the CONTEXT below. If context is insufficient, say so.\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"USER QUESTION:\n{user_question}"
            ),
        },
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            CHAT_ENDPOINT,
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.openai_chat_model,
                "messages": messages,
                "temperature": 0.4,
                "max_tokens": 600,
            },
        )

    # If OpenAI returns 404, it can be either wrong endpoint OR model not found.
    if resp.status_code == 404:
        detail = None
        err_json = None
        try:
            err_json = resp.json()
        except Exception:
            err_json = None

        if isinstance(err_json, dict) and "error" in err_json:
            err = err_json.get("error") or {}
            code = (err.get("code") or "").lower()
            message = (err.get("message") or "")
            # Common OpenAI response when the model is invalid
            if code == "model_not_found" or "does not exist" in message.lower() or (
                "model" in message.lower() and "not found" in message.lower()
            ):
                raise RuntimeError(
                    f"OpenAI model not found: '{settings.openai_chat_model}'. "
                    "Set OPENAI_CHAT_MODEL to a valid Chat Completions model, e.g. 'gpt-4o-mini' or 'gpt-4o'."
                )
            detail = message or str(err_json)

        raise RuntimeError(
            "OpenAI returned 404 for /chat/completions. "
            "Possible causes: (1) wrong OPENAI_BASE_URL, (2) using Azure OpenAI without correct path, "
            "(3) corporate proxy rewriting the URL, (4) typo in endpoint. "
            f"Current endpoint: {CHAT_ENDPOINT}" + (f" | Detail: {detail}" if detail else "")
        )

    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(
            f"OpenAI chat call failed ({e.response.status_code}): {e.response.text}"
        )

    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
