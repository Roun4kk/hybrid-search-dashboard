#!/bin/bash

echo "Starting Hybrid Search + KPI Dashboard"

# activate virtual environment
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running ingestion..."
python -m backend.app.ingest

echo "Building BM25 index..."
python backend/app/index/index_bm25.py --input data/processed/docs.jsonl --out data/index/bm25

echo "Building vector index..."
python backend/app/index/index_vector.py --input data/processed/docs.jsonl --out data/index/vector

echo "Starting API server..."
uvicorn backend.app.api.main:app --reload &

echo "Starting KPI dashboard..."
streamlit run frontend/dashboard.py

echo "System running!"