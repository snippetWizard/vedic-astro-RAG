# 🌌 Vedic Astrology RAG + Chart Interpreter API  
### ⚡ Powered by FastAPI · OpenAI · ChromaDB  

<p align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/LLM-OpenAI_GPT--5-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/Vector_DB-ChromaDB-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.11+-yellow?style=flat-square" />
</p>

---

### 🧠 Overview

This repository contains a **Retrieval-Augmented Generation (RAG)** system specialized for **Vedic Astrology**.  
It combines **semantic retrieval** (ChromaDB + OpenAI embeddings) with a **personalized astrology chart interpreter** (deterministic host/guest logic).

---

## 🚀 Features

✅ Retrieval-Augmented Q&A using OpenAI embeddings  
✅ Persistent local vector store with **ChromaDB**  
✅ Fully async **FastAPI** backend  
✅ JSON-driven astrology domain knowledge  
✅ Deterministic chart analysis engine  
✅ Docker-ready + easy to extend  

---

## 🧱 Project Structure

```bash
rag_app/
├─ app/
│  ├─ main.py                # App entrypoint
│  ├─ config.py              # Global configuration (.env, models, etc.)
│  ├─ schemas.py             # Request/response models
│  ├─ models_openai.py       # OpenAI embeddings + chat completions
│  ├─ vectorstore.py         # Chroma vector store wrapper
│  ├─ utils_chunk.py         # JSON loader + text chunking utilities
│  ├─ rag_pipeline.py        # Core retrieval + reasoning pipeline
│  ├─ router_chat.py         # RAG chat endpoint (/chat/rag)
│  ├─ logic_interpret.py     # Personalized chart logic (host/guest)
│  ├─ router_chart.py        # Chart analysis endpoint (/chart/analyze)
│  ├─ ingest.py              # One-time data ingestion script
│  └─ domain/                # Astrology JSON knowledge base
│     ├─ astrology_houses.json
│     ├─ astrology_planets.json
│     ├─ planets_in_house.json
│     └─ house_lords.json
├─ requirements.txt
├─ .env
├─ Dockerfile
├─ docker-compose.yml
└─ README.md
⚙️ Setup & Installation
1️⃣ Clone and install dependencies
bash
Copy code
git clone https://github.com/your-username/vedic-rag-api.git
cd vedic-rag-api
pip install -r requirements.txt
2️⃣ Create .env
env
Copy code
OPENAI_API_KEY=sk-your-openai-key
CHROMA_PERSIST_DIR=./chroma_storage
CHROMA_COLLECTION=astrology_knowledge
3️⃣ Ingest domain knowledge
bash
Copy code
python -m app.ingest
✅ This:

Loads JSON data from app/domain/

Generates embeddings using OpenAI

Stores vectors into local ChromaDB (./chroma_storage)

4️⃣ Run the API
bash
Copy code
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Visit:

Swagger Docs: http://localhost:8000/docs

Health Check: http://localhost:8000

🧩 Endpoints
🔮 /chat/rag — Retrieval-Augmented Q&A
POST

Request

json
Copy code
{ "query": "What happens if the Sun is in the 1st house?" }
Response

json
Copy code
{
  "answer": "Sun in the 1st house gives visibility, vitality, and leadership...",
  "retrieved_context_preview": [
    {
      "id": "uuid",
      "score": 0.92,
      "text": "Planet Sun in House 1 ...",
      "meta": { "type": "planet_in_house", "house_number": 1, "planet_name": "Sun" }
    }
  ]
}
🪐 /chart/analyze — Personalized Chart Interpretation
POST

Request

json
Copy code
{
  "name": "Sagar",
  "dob": "1998-09-23",
  "lat": 23.7,
  "long": 88.56,
  "houses": {
    "1": "Sun",
    "2": "Mars",
    "3": "Venus",
    "4": "Saturn",
    "5": "Moon",
    "6": "Jupiter",
    "7": "Jupiter",
    "8": "Rahu",
    "9": "Ketu",
    "10": "Sun",
    "11": "Mars",
    "12": "Venus"
  }
}
Response

json
Copy code
{
  "user": { "name": "Sagar", "dob": "1998-09-23" },
  "interpretations": [
    {
      "house_number": 1,
      "natural_lord": "Mars",
      "occupying_planet": "Sun",
      "interpretation": {
        "summary": "Sun in the 1st house creates a powerful, visible personality.",
        "host_guest_dynamics": "Sun expresses its ego through Mars' drive and assertion.",
        "positive_traits_current": ["Leadership", "Confidence"],
        "negative_traits_current": ["Ego clashes", "Impatience"]
      }
    }
  ]
}
🧩 Module Breakdown
<details> <summary><b>app/main.py</b> – FastAPI Entrypoint</summary>
Initializes the app, includes routers (/chat, /chart), and exposes a root health check.

</details> <details> <summary><b>app/config.py</b> – Environment Configuration</summary>
Loads .env variables using pydantic and defines:

OPENAI_API_KEY

CHROMA_PERSIST_DIR, CHROMA_COLLECTION

Retrieval limits (top_k, max_context_chars)

</details> <details> <summary><b>app/models_openai.py</b> – OpenAI Wrapper</summary>
Methods:

generate_embedding(text) → returns embedding vector

generate_answer(system_prompt, user_question, context) → produces final LLM response

</details> <details> <summary><b>app/vectorstore.py</b> – ChromaDB Wrapper</summary>
Handles:

upsert_chunks(chunks) → store text + embeddings

similarity_search(query, top_k) → semantic retrieval

</details> <details> <summary><b>app/rag_pipeline.py</b> – Retrieval-Augmented Generation</summary>
Combines:

Vector search from Chroma

Context building

GPT-5 reasoning call

Returns both answer + retrieved_context_preview

</details> <details> <summary><b>app/logic_interpret.py</b> – Astrology Logic Engine</summary>
Implements:

PLANET_IN_HOUSE_LIBRARY (interpretation DB)

load_house_lords_map()

interpret_chart() → merges host/guest planetary dynamics and returns a full structured reading.

</details> <details> <summary><b>app/utils_chunk.py</b> – JSON Chunk Loader</summary>
Loads and flattens all domain JSON files into text documents ready for embedding.

</details> <details> <summary><b>app/router_chat.py</b> – /chat/rag Endpoint</summary>
Handles semantic Q&A using run_rag() pipeline.

</details> <details> <summary><b>app/router_chart.py</b> – /chart/analyze Endpoint</summary>
Handles deterministic chart interpretation logic (no LLM).

</details> <details> <summary><b>app/ingest.py</b> – Data Ingestion Script</summary>
One-time operation:

Loads domain JSONs

Creates embeddings

Stores them into ChromaDB
Run via:

bash
Copy code
python -m app.ingest
</details> <details> <summary><b>app/domain/</b> – Knowledge Base</summary>
astrology_houses.json → 12 houses + lords

astrology_planets.json → planet details

planets_in_house.json → combinations

house_lords.json → host/guest relationships

</details>
🧠 Flow Diagrams
RAG Flow
mermaid
Copy code
flowchart TD
A[User Query] -->|POST /chat/rag| B[generate_embedding()]
B --> C[Chroma Similarity Search]
C --> D[Retrieve Top Contexts]
D --> E[Assemble Context + Query]
E --> F[GPT-5 Reasoning]
F --> G[Final Answer + Context Preview]
Chart Interpretation Flow
mermaid
Copy code
flowchart TD
A[User Birth Data + Houses] --> B[load_house_lords_map()]
B --> C[interpret_chart()]
C --> D[Host/Guest Logic]
D --> E[Structured Personality & Traits JSON]
🧰 Developer Commands
Task	Command
Install deps	pip install -r requirements.txt
Ingest domain data	python -m app.ingest
Run API	uvicorn app.main:app --reload
Format code	black app/
View docs	http://localhost:8000/docs

🧭 Extending the System
Add new JSONs → app/domain/ → run python -m app.ingest

Expand PLANET_IN_HOUSE_LIBRARY for richer predictions

Tune retrieval in .env (top_k, max_context_chars)

Swap OpenAI model (in config.py) if you want cheaper or faster inference

🧑‍💻 Maintainer Notes
chroma_storage/ is your local vector DB; do not commit it.

Run ingestion whenever JSONs are updated.

You can deploy via Docker or directly on FastAPI’s Uvicorn server.

🧩 Tech Stack
Layer	Technology	Purpose
Backend	FastAPI	REST API framework
Vector Store	ChromaDB	Local vector embeddings store
LLM API	OpenAI GPT-5 / Embeddings	Semantic reasoning & context generation
Data	JSON	Transparent, version-controlled knowledge base
Runtime	Python 3.11+	Core language

💫 Example Query
bash
Copy code
curl -X POST http://localhost:8000/chat/rag \
-H "Content-Type: application/json" \
-d '{"query": "Explain Mercury in the first house"}'


## 🧾 License

MIT © 2025 — Developed with ❤️ and FastAPI.

---

**Author:** [Sagar Paul](https://github.com/snippetWizard)  
**Version:** `v1.1.0`  
**Repo:** [vedic-rag-api](https://github.com/snippetWizard/vedic-astro-RAG)`