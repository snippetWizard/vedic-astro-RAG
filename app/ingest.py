import asyncio
from .utils_chunk import load_domain_jsons, flatten_astrology_docs
from .vectorstore import vector_store


async def ingest_domain_knowledge():
    """
    1. Load domain JSON files from /app/domain
    2. Chunk them
    3. Upsert into Chroma
    """
    print("[INGEST] Loading domain JSON...")
    docs = load_domain_jsons()
    chunks = flatten_astrology_docs(docs)

    if not chunks:
        raise RuntimeError("No chunks generated from domain JSON. Check data format.")

    print(f"[INGEST] Upserting {len(chunks)} chunks into Chroma...")
    await vector_store.upsert_chunks(chunks)

    print("[INGEST] DONE ✅")


if __name__ == "__main__":
    asyncio.run(ingest_domain_knowledge())
