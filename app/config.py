import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    openai_chat_model: str = Field(
        default="gpt-4o-mini",
        description="OpenAI chat model ID for final answer"
    )
    openai_embedding_model: str = Field(
        default="text-embedding-3-large",
        description="Embedding model for semantic retrieval"
    )
    chroma_persist_dir: str = Field(
        default="./chroma_storage",
        description="Local directory where ChromaDB persists the collection"
    )
    chroma_collection: str = Field(
        default="astrology_knowledge",
        description="ChromaDB collection name"
    )
    top_k: int = Field(default=5, description="How many chunks to retrieve per query")
    max_context_chars: int = Field(
        default=4000,
        description="Hard cap on combined retrieved context passed to LLM"
    )


def get_settings() -> Settings:
    return Settings(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        # Allow overriding models via env vars if provided
        openai_chat_model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        openai_embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
        chroma_persist_dir=os.getenv("CHROMA_PERSIST_DIR", "./chroma_storage"),
        chroma_collection=os.getenv("CHROMA_COLLECTION", "astrology_knowledge"),
    )


settings = get_settings()
