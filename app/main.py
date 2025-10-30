from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .router_chat import router as chat_router  # RAG Q&A route
# from .router_chart import router as chart_router  # NEW personalized chart route

app = FastAPI(
    title="Vedic Astrology RAG API",
    version="1.1.0",
    description="RAG + personalized chart interpretation API"
)

app.include_router(chat_router)
# app.include_router(chart_router)

@app.get("/", tags=["health"])
async def root():
    return JSONResponse({"status": "ok", "service": "vedic-rag"})

