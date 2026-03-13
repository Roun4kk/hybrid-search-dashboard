#!/bin/bash

echo "Starting Hybrid Search + KPI Dashboard"

# activate virtual environment (Windows path)
source .venv/Scripts/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running ingestion..."
python -m backend.app.ingest --input data/raw --out data/processed/docs.jsonl

echo "Building BM25 index..."
python -m backend.app.index.index_bm25 --input data/processed/docs.jsonl --out data/index/bm25

echo "Building vector index..."
python -m backend.app.index.index_vector --input data/processed/docs.jsonl --out data/index/vector

echo "Starting API server..."
uvicorn backend.app.api.main:app --reload &

echo "Starting KPI dashboard..."
streamlit run frontend/dashboard.py

echo "-----------------------------------"
echo "System ready!"
echo "API: http://127.0.0.1:8000/docs"
echo "Dashboard: http://localhost:8501"
echo "-----------------------------------"