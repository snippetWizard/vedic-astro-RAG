import pytest


@pytest.mark.asyncio
async def test_ingest_calls_vectorstore(monkeypatch):
    # Avoid reading files; patch loaders to return a prepared chunk list
    sample_chunks = [
        {"text": "House 1 ...", "metadata": {"type": "house", "house_number": 1}}
    ]

    import app.ingest as ingest

    def fake_load_domain_jsons():
        return [
            {"source_file": "app/domain/astrology_houses.json", "data": {"dummy": True}}
        ]

    def fake_flatten_astrology_docs(docs):
        return sample_chunks

    calls = {"upsert": 0}

    class _FakeVS:
        async def upsert_chunks(self, chunks):
            calls["upsert"] += 1
            assert chunks == sample_chunks

    monkeypatch.setattr(ingest, "load_domain_jsons", fake_load_domain_jsons)
    monkeypatch.setattr(ingest, "flatten_astrology_docs", fake_flatten_astrology_docs)
    monkeypatch.setattr(ingest, "vector_store", _FakeVS())

    await ingest.ingest_domain_knowledge()
    assert calls["upsert"] == 1

