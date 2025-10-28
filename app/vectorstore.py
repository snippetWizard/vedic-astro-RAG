from typing import List, Dict, Any
import uuid
import chromadb
from chromadb.config import Settings as ChromaSettings
from .config import settings
from .models_openai import generate_embedding


class VectorStore:
    """
    Wrapper around ChromaDB.

    Responsibilities:
    - Initialize (or open) a persistent collection
    - Insert (upsert) text chunks with embeddings
    - Perform similarity search
    """

    def __init__(self):
        # Create / open persistent ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space": "cosine"}  # cosine similarity
        )

    async def upsert_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Insert a batch of chunks.
        Each chunk:
        {
          "text": str,
          "metadata": {...}
        }

        For Chroma, we insert:
        - ids[]
        - documents[]
        - metadatas[]
        - embeddings[]

        We generate embeddings here using OpenAI.
        """
        ids: List[str] = []
        documents: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        embeddings: List[List[float]] = []

        for ch in chunks:
            doc_id = str(uuid.uuid4())
            ids.append(doc_id)
            documents.append(ch["text"])
            metadatas.append(ch["metadata"])

            emb = await generate_embedding(ch["text"])
            embeddings.append(emb)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    async def similarity_search(
        self, query: str, top_k: int
    ) -> List[Dict[str, Any]]:
        """
        - embed query
        - run similarity search in Chroma
        - return list of normalized result dicts
        """
        query_emb = await generate_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )

        # Chroma returns lists for each field, shape [ [item1,item2,...] ]
        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        out = []
        for i in range(len(ids)):
            out.append(
                {
                    "id": ids[i],
                    "score": float(dists[i]) if dists is not None else 0.0,
                    "text": docs[i],
                    "meta": metas[i],
                }
            )
        return out


# singleton-ish
vector_store = VectorStore()
