from typing import List
from .config import settings
from .vectorstore import vector_store
from .models_openai import generate_answer
from .schemas import RetrievedChunk


SYSTEM_PROMPT = (
    "You are a Retrieval-Augmented Vedic Astrology Knowledge Assistant.\n"
    "- You answer based ONLY on provided context.\n"
    "- You avoid medical/political/legal predictions.\n"
    "- If context is missing, say so honestly.\n"
    "- Be clear and human, not robotic."
)


async def run_rag(query: str) -> (str, List[RetrievedChunk]):
    """
    1. Retrieve top_k matches from Chroma.
    2. Build context (truncate to max_context_chars).
    3. Call GPT-5 Thinking.
    4. Return final answer + preview chunks.
    """

    results = await vector_store.similarity_search(
        query=query,
        top_k=settings.top_k
    )

    # Build final context for the LLM
    context_parts = []
    total_chars = 0
    for r in results:
        block = f"[source]\n{r['text']}\n"
        if total_chars + len(block) > settings.max_context_chars:
            break
        context_parts.append(block)
        total_chars += len(block)

    context_str = "\n\n".join(context_parts)

    llm_answer = await generate_answer(
        system_prompt=SYSTEM_PROMPT,
        user_question=query,
        context=context_str
    )

    # Return previews so UI/debug can show what was used
    retrieved_preview: List[RetrievedChunk] = []
    for r in results:
        retrieved_preview.append(
            RetrievedChunk(
                id=r["id"],
                score=r["score"],
                text=r["text"][:250],
                meta=r["meta"]
            )
        )

    return llm_answer, retrieved_preview
