import os
import importlib
import pytest


class _FakeResp:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text

    def json(self):
        return self._json

    def raise_for_status(self):
        import httpx

        if self.status_code >= 400:
            raise httpx.HTTPStatusError("error", request=None, response=self)


class _FakeAsyncClient404ModelNotFound:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def post(self, url, headers=None, json=None):
        return _FakeResp(
            status_code=404,
            json_data={
                "error": {
                    "code": "model_not_found",
                    "message": "The model does not exist",
                }
            },
            text="The model does not exist",
        )


class _FakeAsyncClientEmbeddingOK:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def post(self, url, headers=None, json=None):
        return _FakeResp(status_code=200, json_data={"data": [{"embedding": [0.1, 0.2]}]})


@pytest.mark.asyncio
async def test_generate_answer_404_model_not_found(monkeypatch):
    # Import target module
    import app.models_openai as mo

    # Patch httpx.AsyncClient to our fake 404 client
    monkeypatch.setattr(mo.httpx, "AsyncClient", _FakeAsyncClient404ModelNotFound)

    with pytest.raises(RuntimeError) as ei:
        await mo.generate_answer("sys", "q", "ctx")

    assert "model not found" in str(ei.value).lower()


@pytest.mark.asyncio
async def test_generate_embedding_success(monkeypatch):
    import app.models_openai as mo

    # Patch httpx.AsyncClient to return a simple vector
    monkeypatch.setattr(mo.httpx, "AsyncClient", _FakeAsyncClientEmbeddingOK)

    vec = await mo.generate_embedding("hello world")
    assert isinstance(vec, list) and vec == [0.1, 0.2]


def test_base_url_guard_appends_v1(monkeypatch):
    # Ensure that if OPENAI_BASE_URL misses /v1, module computes it
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.com")
    # Reload module so constants recompute
    import app.models_openai as mo

    importlib.reload(mo)

    assert mo.CHAT_ENDPOINT.endswith("/v1/chat/completions")

