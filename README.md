<div align="center">
  <h1>🔗 GraphRAG</h1>
  <p><em>A multimodal retrieval-augmented generation system<br/>with graph-based second-hop expansion</em></p>
  <br/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  &nbsp;
  <img src="https://img.shields.io/badge/ChromaDB-FF6B35?style=for-the-badge&logoColor=white" />
  &nbsp;
  <img src="https://img.shields.io/badge/CLIP-412991?style=for-the-badge&logo=openai&logoColor=white" />
  &nbsp;
  <img src="https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</div>

<br/>



## Overview

**GraphRAG** combines dense vector retrieval, CLIP-based image-text search, and entity graph expansion into a single unified pipeline — so your queries don't just find relevant chunks, they traverse the knowledge graph to surface second-hop context that flat RAG misses.

Works out of the box with a demo dataset. Drop in an OpenAI key for grounded LLM answers, or run fully offline in extractive fallback mode.

<br/>

## Features

| | |
|---|---|
| 📄 **Dense text retrieval** | Chunked document search via sentence-transformers + ChromaDB |
| 🖼️ **Multimodal retrieval** | Image-text search using CLIP embeddings |
| 🕸️ **Graph expansion** | GraphRAG-style second-hop traversal over entity relationships |
| 🤖 **LLM answer generation** | Grounded answers via OpenAI when a key is configured |
| 🔌 **Fallback mode** | Extractive answers with no API key required |
| ⚡ **FastAPI endpoints** | Clean REST API for ingestion and querying |
| 🗂️ **Demo dataset** | Ready-to-run example data included |

<br/>

## How It Works

```
Query
  │
  ├─► Dense retrieval (sentence-transformers)   ──► Top-K text chunks
  │
  ├─► CLIP retrieval (image-text embeddings)    ──► Top-K images
  │
  └─► Entity graph expansion                    ──► Second-hop context
            │
            ▼
      LLM synthesis  (or extractive fallback)
            │
            ▼
        Grounded Answer
```

<br/>

## Project Structure

```
graphrag/
├── app/                    # FastAPI application & pipeline logic
├── data/
│   └── demo/               # Demo dataset for quickstart
├── scripts/                # Ingestion & utility scripts
├── tests/                  # Test suite
├── requirements.txt
└── .env.example
```

<br/>

## Quickstart

### 1 — Create environment

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** On first run, model downloads (sentence-transformers, CLIP) may take a few minutes.

### 2 — Configure environment

```bash
cp .env.example .env
```

Open `.env` and add your key for LLM-powered answers:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

No key? No problem — the system runs in **extractive fallback mode** automatically.

### 3 — Start the server

```bash
uvicorn app.main:app --reload
```

### 4 — Ingest the demo dataset

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"data_dir":"./data/demo"}'
```

### 5 — Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How does graph expansion help retrieval?",
    "top_k_text": 5,
    "top_k_image": 2,
    "graph_hops": 1,
    "use_multimodal": true
  }'
```

<br/>

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/ingest` | Ingest documents from a directory |
| `POST` | `/query` | Run a multimodal GraphRAG query |

<br/>

## Example Queries

```
"What does the project say about GraphRAG?"
"How are images used in the retrieval pipeline?"
"What is the role of dense retrieval before graph expansion?"
```

<br/>

## Storage & Persistence

| Layer | Storage |
|-------|---------|
| Vector store | `data/processed/chroma/` (persisted on disk) |
| Entity graph | In-memory, rebuilt on each ingestion |

<br/>

## Roadmap

- [ ] Replace simple entity extractor with spaCy or LLM-based NER
- [ ] Add BM25 / hybrid sparse+dense retrieval
- [ ] Add cross-encoder reranker for result reordering
- [ ] Add image captioning for richer multimodal evidence
- [ ] Migrate graph storage to Neo4j for larger corpora

<br/>



<div align="center">

</div>
