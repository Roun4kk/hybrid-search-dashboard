# System Architecture

The Hybrid Search + KPI Dashboard system is composed of several modular components.

---

## High Level Architecture

User Query
↓
FastAPI Backend
↓
Hybrid Search Engine
↓
BM25 Index + Vector Index
↓
Document Corpus

Metrics and logs are stored separately in SQLite.

---

## Component Overview

### 1. Data Ingestion

Location:

backend/app/ingest/

Function:

- Reads raw text documents
- Converts them into structured JSONL format
- Stores normalized documents for indexing

Output file:

data/processed/docs.jsonl

---

### 2. BM25 Index

Location:

backend/app/search/bm25.py

Function:

- Tokenizes document corpus
- Builds lexical index using BM25
- Supports keyword-based ranking

Stored in:

data/index/bm25/

---

### 3. Vector Index

Location:

backend/app/search/vector.py

Function:

- Generates sentence embeddings
- Builds FAISS vector index
- Enables semantic similarity search

Stored in:

data/index/vector/

---

### 4. Hybrid Search

Location:

backend/app/search/hybrid.py

Function:

- Combines BM25 and vector scores
- Applies normalization
- Produces final ranked results

---

### 5. Search API

Location:

backend/app/api/main.py

Endpoints:

GET /health

POST /search

Returns ranked results with score breakdown.

---

### 6. Query Logging

Location:

backend/app/db/db.py

Function:

Stores search queries and metadata in SQLite.

Stored in:

data/metrics/search_logs.db

---

### 7. Evaluation Harness

Location:

backend/app/eval/evaluate.py

Metrics:

- nDCG@10
- Recall@10
- MRR@10

Used to measure ranking quality across experiments.

---

## Data Flow

Raw Documents
↓
Ingestion
↓
Processed JSONL
↓
BM25 Index + Vector Index
↓
Hybrid Search Engine
↓
API Results
↓
Metrics Logging