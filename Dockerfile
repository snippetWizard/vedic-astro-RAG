# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Ensure stdout/stderr are unbuffered, avoid .pyc, and keep pip lean
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (minimal). Uncomment if you need build tools for native wheels.
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#  && rm -rf /var/lib/apt/lists/*

# Install Python deps first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY README.md ./README.md

# Create a volume mount point for Chroma persistence
VOLUME ["/app/chroma_storage"]

EXPOSE 8000

# Default command: run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

