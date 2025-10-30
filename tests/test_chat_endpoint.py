from fastapi.testclient import TestClient
import asyncio


def test_chat_rag_endpoint_happy_path(monkeypatch):
    # Patch the run_rag function used inside the router to avoid external calls
    async def fake_run_rag(query: str):
        return (
            "Astrology answer based on retrieved context.",
            [
                {
                    "id": "abc",
                    "score": 0.1,
                    "text": "Planet Sun in House 1 ...",
                    "meta": {"type": "planet_in_house", "house_number": 1, "planet_name": "Sun"},
                }
            ],
        )

    import app.router_chat as router_chat

    monkeypatch.setattr(router_chat, "run_rag", fake_run_rag)

    from app.main import app

    client = TestClient(app)
    res = client.post("/chat/rag", json={"query": "What is Sun in 1st house?"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data and isinstance(data["answer"], str)
    assert "retrieved_context_preview" in data and isinstance(
        data["retrieved_context_preview"], list
    )

