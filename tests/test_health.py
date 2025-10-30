from fastapi.testclient import TestClient


def test_root_health():
    from app.main import app

    client = TestClient(app)
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data.get("status") == "ok"
    assert data.get("service") == "vedic-rag"

