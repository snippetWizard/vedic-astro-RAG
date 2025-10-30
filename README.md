# Vedic Astrology RAG API

FastAPI backend that answers Vedic Astrology questions using Retrieval‑Augmented Generation (RAG) over a small JSON knowledge base. It uses ChromaDB for semantic search and OpenAI for embeddings and chat completions.

---

**Why RAG for this data**
- Grounded answers: responses are constrained to your vetted JSON knowledge, reducing hallucinations.
- Easy updates: edit JSON files and re‑ingest — no fine‑tuning or retraining.
- Transparent: API returns a preview of the exact chunks used.
- Efficient: only the most relevant snippets are sent to the model, saving tokens and cost.

---

**Installation**
- Prereqs: Python 3.11+
- Create a virtual environment and install dependencies:
  - Windows PowerShell: `python -m venv .venv && . .venv/Scripts/activate`
  - Then: `pip install -r requirements.txt`
- Create `.env` with at least:
  - `OPENAI_API_KEY=sk-your-key`
  - Optional: `OPENAI_CHAT_MODEL=gpt-4o-mini`
  - Optional: `OPENAI_EMBEDDING_MODEL=text-embedding-3-large`
  - Optional: `CHROMA_PERSIST_DIR=./chroma_storage`, `CHROMA_COLLECTION=astrology_knowledge`
- Ingest the domain knowledge into ChromaDB:
  - `python -m app.ingest`
- Run the API:
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
  - Docs: http://localhost:8000/docs

---

**Request/Response (human words)**
- You send a natural language question to the server.
- The app searches its local astrology knowledge for the most relevant passages.
- It asks OpenAI to write an answer using only those passages as context.
- You get back the final answer plus a short preview of the passages used.

Example request
```bash
curl -X POST http://localhost:8000/chat/rag \
  -H "Content-Type: application/json" \
  -d '{"query": "What does Sun in the 1st house mean?"}'
```

Example response
```json
{
  "answer": "Sun in the 1st house emphasizes visibility, vitality, and leadership...",
  "retrieved_context_preview": [
    {
      "id": "...",
      "score": 0.12,
      "text": "Planet Sun in House 1 ...",
      "meta": { "type": "planet_in_house", "house_number": 1, "planet_name": "Sun" }
    }
  ]
}
```

---

**Application Flow — Files**
- `app/main.py` — boot FastAPI and mount routes.
- `app/router_chat.py` — define POST `/chat/rag` endpoint.
- `app/rag_pipeline.py` — orchestrate retrieval and generation.
- `app/vectorstore.py` — ChromaDB wrapper (persisted collection, upserts, search).
- `app/models_openai.py` — OpenAI calls for embeddings and chat completions.
- `app/utils_chunk.py` — load JSON and convert to retrievable text chunks.
- `app/ingest.py` — one‑shot ingestion script to build the vector store.
- `app/logic_interpret.py` — deterministic astrology interpretation helpers (separate from `/chat/rag`).
- `app/schemas.py` — Pydantic request/response schemas.

---

**Application Flow — Methods**
- Ingestion (`python -m app.ingest`)
  - `utils_chunk.load_domain_jsons()` → read JSONs under `app/domain/`.
  - `utils_chunk.flatten_astrology_docs()` → emit `{text, metadata}` chunks.
  - `vectorstore.upsert_chunks(chunks)` → embed each chunk via `models_openai.generate_embedding()` and write into Chroma.

- Query (`POST /chat/rag`)
  - `router_chat.rag_chat_endpoint()` → entrypoint for Q&A.
  - `rag_pipeline.run_rag(query)`
    - `vectorstore.similarity_search(query, top_k)` → embed query via `models_openai.generate_embedding()` and search Chroma.
    - Build a context string from the top results (capped by `max_context_chars`).
    - `models_openai.generate_answer(system_prompt, user_question, context)` → OpenAI chat completion using only the retrieved context.
    - Return final answer + retrieved chunk preview.

What runs where
- Retrieval is local (ChromaDB on disk).
- Embeddings and the final answer come from OpenAI.
- Models are configurable via env; defaults are `gpt-4o-mini` and `text-embedding-3-large`.

---

**Configuration Notes**
- `OPENAI_BASE_URL` is optional. If you point at `api.openai.com`, the app ensures `/v1` is present.
- Azure/OpenAI proxies may require a custom base URL and `api-version`. Ask if you want that wired in.
- Tuning knobs in `app/config.py`: `top_k` and `max_context_chars`.

---

**Endpoint**
- `POST /chat/rag`
  - Request: `{ "query": "..." }`
  - Response: `{ "answer": "...", "retrieved_context_preview": [...] }`

---

**Tech Stack**
- FastAPI (Python) for the API
- ChromaDB for local vector search
- OpenAI for embeddings and chat completions

---

License: MIT

---

Docker usage
- Build image: `docker build -t astrology-rag:latest .`
- Run API: `docker run --rm -p 8000:8000 --env-file .env -v ${PWD}/chroma_storage:/app/chroma_storage astrology-rag:latest`
- With Docker Compose:
  - Start API: `docker compose up --build -d api`
  - One-shot ingestion: `docker compose run --rm ingest`
    - This runs `python -m app.ingest` inside the container and exits.
    - The `chroma_storage` volume is persisted at `./chroma_storage` on the host.

---

Publish images
- Docker Hub (manual):
  - `docker login`
  - `docker build -t <dockerhub-username>/astrology-rag:latest .`
  - `docker push <dockerhub-username>/astrology-rag:latest`
- GitHub Container Registry (manual):
  - Create a classic Personal Access Token with `write:packages` scope or use `gh auth login`.
  - `echo $CR_PAT | docker login ghcr.io -u <github-username> --password-stdin`
  - `docker tag astrology-rag:latest ghcr.io/<owner>/<repo>:latest`
  - `docker push ghcr.io/<owner>/<repo>:latest`
- GitHub Actions (automated):
  - Workflow file: `.github/workflows/docker-publish.yml` builds on pushes to `main` and tags like `v*`.
  - It publishes to GHCR as `ghcr.io/<owner>/<repo>:<tag>` and `:latest` on the default branch.
  - Optional: add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repo secrets to also push to Docker Hub (see commented line in the workflow).

---

Local test and Docker Hub publish
- Build local image:
  - `docker build -t astrology-rag:latest .`
- Create a persistent volume for Chroma (recommended on Windows):
  - `docker volume create rag_chroma`
- Ingest knowledge base (one-shot):
  - `docker run --rm --env-file .env -v rag_chroma:/app/chroma_storage astrology-rag:latest python -m app.ingest`
- Run the API:
  - `docker run --rm -d --name rag_api -p 8000:8000 --env-file .env -v rag_chroma:/app/chroma_storage astrology-rag:latest`
- Test endpoints:
  - Health: `curl http://localhost:8000/`
  - Chat (PowerShell):
    - `$body = @{ query = "What does Sun in the 1st house mean?" } | ConvertTo-Json`
    - `Invoke-RestMethod -Method Post -Uri http://localhost:8000/chat/rag -ContentType 'application/json' -Body $body`
- Stop API:
  - `docker stop rag_api`

Publish to Docker Hub (manual)
- Login:
  - `docker login`
- Tag and push latest:
  - `docker tag astrology-rag:latest <dockerhub-username>/astrology-rag:latest`
  - `docker push <dockerhub-username>/astrology-rag:latest`
- Optional version tag:
  - PowerShell: `$VERSION = "v0.1.0"`
  - `docker tag astrology-rag:latest <dockerhub-username>/astrology-rag:$VERSION`
  - `docker push <dockerhub-username>/astrology-rag:$VERSION`

Automated publish via GitHub Actions
- Workflow: `.github/workflows/docker-publish.yml` builds on pushes to `main/master` and tags `v*`.
- Pushes to:
  - GHCR: `ghcr.io/<owner>/<repo>:<tag>` and `:latest` on default branch.
  - Docker Hub: `docker.io/<DOCKERHUB_USERNAME>/astrology-rag:<tag>` (requires repo secrets).
- Required repo secrets for Docker Hub:
  - `DOCKERHUB_USERNAME`: your Docker Hub username.
  - `DOCKERHUB_TOKEN`: a Docker Hub Access Token (create under Docker Hub → Account Settings → Security → New Access Token).
- Multi-arch (optional): edit workflow `platforms` to `linux/amd64,linux/arm64`.
- CI tests: On push/PR to `main/master`, `pytest` runs first. Image publish only occurs if tests pass and the event is a push (not a PR).
