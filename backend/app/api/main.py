from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.search.hybrid import HybridSearch
from backend.app.db.db import init_db, log_query
import sqlite3

app = FastAPI(title="Hybrid Search + KPI Dashboard", version="1.0")

init_db()
search_engine = HybridSearch()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    alpha: float = 0.5


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search")
def search(req: SearchRequest):

    results = search_engine.search(
        req.query,
        req.top_k,
        req.alpha
    )

    # determine if results are meaningful
    max_score = max([r["hybrid_score"] for r in results]) if results else 0

    if max_score < 0.2:
        result_count = 0
    else:
        result_count = len(results)

    log_query(
        req.query,
        req.top_k,
        req.alpha,
        result_count
    )

    return {"results": results}

@app.get("/metrics")
def metrics():

    conn = sqlite3.connect("data/metrics/search_logs.db")
    cur = conn.cursor()

    # total queries
    cur.execute("SELECT COUNT(*) FROM search_logs")
    total_queries = cur.fetchone()[0]

    # top queries
    cur.execute("""
        SELECT query, COUNT(*) as count
        FROM search_logs
        GROUP BY query
        ORDER BY count DESC
        LIMIT 5
    """)
    top_queries = cur.fetchall()

    # zero result queries
    cur.execute("""
        SELECT query, COUNT(*)
        FROM search_logs
        WHERE result_count = 0
        GROUP BY query
        ORDER BY COUNT(*) DESC
    """)
    zero_results = cur.fetchall()

    conn.close()

    return {
        "total_queries": total_queries,
        "top_queries": top_queries,
        "zero_result_queries": zero_results
    }