import os


def pytest_configure(config):
    # Minimal environment so config/settings can import without ValidationError
    os.environ.setdefault("OPENAI_API_KEY", "sk-test-key")
    os.environ.setdefault("CHROMA_PERSIST_DIR", "./.test_chroma_storage")
    os.environ.setdefault("CHROMA_COLLECTION", "astrology_knowledge_test")
    os.environ.setdefault("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    os.environ.setdefault("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")

