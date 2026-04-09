# OmniGraphRAG

A runnable **GraphRAG + multimodal RAG** project built with FastAPI, ChromaDB, sentence-transformers, and CLIP.

## Features
- Dense text retrieval over chunked documents
- Image-text retrieval using CLIP embeddings
- Entity graph expansion (GraphRAG-style second-hop retrieval)
- Grounded answer generation using an LLM when configured
- Fallback extractive answer mode when no API key is available
- FastAPI endpoints for ingestion and querying
- Demo dataset included

## Project structure

```text
omnigraphrag_project/
├── app/
├── data/demo/
├── scripts/
├── tests/
├── requirements.txt
└── .env.example
```

## Quickstart

### 1) Create environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment

```bash
cp .env.example .env
```

Add your API key if you want LLM answers:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

If you do not set an API key, the project still runs in **fallback extractive mode**.

### 3) Start the server

```bash
uvicorn app.main:app --reload
```

### 4) Ingest the demo dataset

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"data_dir":"./data/demo"}'
```

### 5) Query the system

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"How does graph expansion help retrieval?","top_k_text":5,"top_k_image":2,"graph_hops":1,"use_multimodal":true}'
```

## Endpoints
- `GET /health`
- `POST /ingest`
- `POST /query`

## Example questions
- What does the project say about GraphRAG?
- How are images used in the retrieval pipeline?
- What is the role of dense retrieval before graph expansion?

## Notes
- On first run, model downloads may take time.
- Chroma data is persisted under `data/processed/chroma`.
- The graph is currently in-memory and rebuilt on ingestion.

## Suggested improvements
- Replace the simple entity extractor with spaCy or LLM-based extraction
- Add BM25 or hybrid sparse+dense retrieval
- Add a cross-encoder reranker
- Add image captioning for richer multimodal evidence
- Move graph storage to Neo4j for larger corpora
