# Hybrid Search + KPI Dashboard

A hybrid search system combining lexical search (BM25) and semantic search (vector embeddings) with real-time analytics.

## Features
- Document ingestion pipeline
- BM25 lexical search
- Semantic vector search using SentenceTransformers + FAISS
- Hybrid ranking combining BM25 and vector similarity
- FastAPI search API
- Query logging using SQLite
- KPI analytics dashboard built with Streamlit
- Metrics including:
  - Total queries
  - Top queries
  - Zero-result queries
- Automation script for one-command startup

## Evaluation Results

Dataset: 300 synthetic documents  
Queries: 25 evaluation queries  

Metrics:

| Metric | Score |
|------|------|
| nDCG@10 | 0.65 |
| Recall@10 | 1.00 |
| MRR | 0.59 |

## Run the system

Clone the repository and run:

```bash
./up.sh