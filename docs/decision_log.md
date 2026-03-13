# Decision Log

This document records key architectural and implementation decisions made during development of the Hybrid Search + KPI Dashboard system.

---

## Hybrid Retrieval Strategy

The system uses a hybrid search approach combining lexical search (BM25) and semantic search (vector embeddings).

### Rationale
- BM25 performs well for exact keyword matches.
- Semantic embeddings capture contextual meaning of queries.
- Combining both improves overall retrieval quality.

The hybrid score is computed as:

hybrid_score = alpha * normalized_bm25 + (1 - alpha) * normalized_vector

Where alpha controls the balance between lexical and semantic relevance.

---

## Choice of BM25 Library

Library used: `rank-bm25`

Reasons:
- Lightweight and CPU-friendly
- Easy integration with Python
- Suitable for small and medium document collections

---

## Choice of Embedding Model

Model used:

sentence-transformers/all-MiniLM-L6-v2

Reasons:
- Small (~90MB)
- Fast CPU inference
- Good semantic search performance

---

## Vector Search Engine

Library used: `FAISS`

Reasons:
- Efficient similarity search
- Works well with dense embeddings
- Fully CPU compatible

---

## API Framework

Framework used: `FastAPI`

Reasons:
- High performance
- Automatic OpenAPI documentation
- Simple integration with Python data models

---

## Database Choice

Database used: `SQLite`

Reasons:
- Lightweight
- No external dependencies
- Suitable for storing query logs and metrics locally

---

## Frontend Strategy

Initial development focuses on backend search functionality.

Dashboard visualization will be implemented using a lightweight UI framework to display metrics such as:

- Search volume
- Top queries
- Zero-result queries
- Evaluation results

---

## CPU-only Requirement

All system components were selected to run efficiently on CPU-only environments.

This ensures reproducibility on typical laptops without requiring GPU acceleration.