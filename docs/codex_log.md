# Codex Prompt Log

This document records incremental prompts used with a coding assistant during development of the Hybrid Search + KPI Dashboard system.

Each prompt corresponds to a small development step and was reviewed and edited manually before committing.

---

## Prompt 1 — Project structure

Prompt:
Create a Python backend project structure for a search system with modules for ingest, index, search, and API using FastAPI.

Output used:
Generated folder structure under backend/app with modules for ingestion, indexing, search logic, and API endpoints.

Manual edits:
Adjusted directory structure and added __init__.py files.

---

## Prompt 2 — Document ingestion pipeline

Prompt:
Write a Python script that reads .txt documents from a folder and converts them into JSONL format with fields doc_id, title, text, source, and created_at.

Output used:
Created ingest.py with read_documents() and write_jsonl() functions.

Manual edits:
Added argparse support and directory creation for output.

---

## Prompt 3 — BM25 lexical search

Prompt:
Implement BM25 indexing using rank-bm25. Provide a BM25Index class with build(), save(), load(), and search() methods.

Output used:
Used BM25Okapi from rank_bm25 to score documents.

Manual edits:
Added tokenization and pickle-based index storage.

---

## Prompt 4 — Vector semantic search

Prompt:
Implement semantic search using sentence-transformers and FAISS. Build embeddings for documents and store them in a FAISS index.

Output used:
Created VectorIndex class with embedding generation and FAISS indexing.

Manual edits:
Added save/load functionality and float32 conversion for FAISS compatibility.

---

## Prompt 5 — Hybrid search ranking

Prompt:
Combine BM25 and vector search results using hybrid scoring with configurable alpha weighting.

Output used:
Created HybridSearch class.

Manual edits:
Added min-max normalization and final ranking sorting.

---

## Prompt 6 — FastAPI search endpoint

Prompt:
Create a FastAPI endpoint POST /search that accepts query, top_k, and alpha parameters and returns hybrid search results.

Output used:
Implemented request schema with Pydantic and integrated HybridSearch.

Manual edits:
Added result formatting and error handling.

---

## Prompt 7 — Query logging

Prompt:
Implement SQLite logging for search queries including query text, top_k, alpha, result_count, and timestamp.

Output used:
Created db.py with init_db() and log_query() functions.

Manual edits:
Integrated logging inside /search endpoint.

---

## Prompt 8 — Evaluation harness

Prompt:
Implement evaluation metrics for search ranking including nDCG@10, Recall@10, and MRR@10.

Output used:
Created evaluation script under backend/app/eval.

Manual edits:
Added small test query set and aggregated metric output.