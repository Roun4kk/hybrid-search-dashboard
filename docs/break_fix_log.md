# Break/Fix Log

This document records intentionally introduced system failures and the debugging process used to recover from them.

---

## Scenario 1 — Vector Index Dimension Mismatch

### Injected Failure

The embedding model was changed without rebuilding the vector index.

This caused FAISS to receive embeddings with a different dimensionality than the stored index.

### Observed Behavior

Vector search raised a runtime error due to dimension mismatch.

### Diagnosis

The FAISS index was built using a previous embedding model.

The new model produced vectors with different dimensionality.

### Fix

Added validation to ensure the embedding model used for querying matches the model used during index creation.

If mismatch is detected, the system rebuilds the index.

---

## Scenario 2 — SQLite Schema Change

### Injected Failure

The search_logs table schema was modified by adding a NOT NULL column without migration.

### Observed Behavior

API requests failed when attempting to log queries.

### Diagnosis

Existing database schema did not match the updated code.

### Fix

Added schema initialization logic in init_db() to safely create or update the database structure.

---

## Scenario 3 — Hybrid Score Normalization Bug

### Injected Failure

Normalization code was modified so that division by zero occurred when all scores were identical.

### Observed Behavior

Hybrid scores returned NaN values.

Ranking results became unstable.

### Diagnosis

Normalization denominator became zero when min_score == max_score.

### Fix

Added safe normalization condition:

if max_s - min_s == 0:
    return [0 for _ in scores]

This prevents division-by-zero errors.