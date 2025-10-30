import pytest


@pytest.mark.asyncio
async def test_run_rag_builds_context_and_returns_preview(monkeypatch):
    # Arrange: stub similarity search results
    fake_results = [
        {
            "id": "1",
            "score": 0.11,
            "text": "Planet Sun in the 1st House indicates visibility.",
            "meta": {"type": "planet_in_house", "house_number": 1, "planet_name": "Sun"},
        },
        {
            "id": "2",
            "score": 0.12,
            "text": "House 1 relates to identity and presence.",
            "meta": {"type": "house", "house_number": 1},
        },
    ]

    import app.rag_pipeline as rp

    # Patch vector_store.similarity_search
    async def fake_similarity_search(query: str, top_k: int):
        return fake_results

    monkeypatch.setattr(rp.vector_store, "similarity_search", fake_similarity_search)

    # Capture context passed to OpenAI
    captured = {}

    async def fake_generate_answer(system_prompt: str, user_question: str, context: str) -> str:
        captured["system_prompt"] = system_prompt
        captured["user_question"] = user_question
        captured["context"] = context
        return "final-answer"

    monkeypatch.setattr(rp, "generate_answer", fake_generate_answer)

    # Act
    answer, preview = await rp.run_rag("Explain Sun in 1st house")

    # Assert
    assert answer == "final-answer"
    assert isinstance(preview, list) and len(preview) == len(fake_results)
    # Ensure both chunks made it into the assembled context
    assert "Planet Sun in the 1st House" in captured.get("context", "")
    assert "House 1 relates to identity" in captured.get("context", "")

