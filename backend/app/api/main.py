from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.search.hybrid import HybridSearch
from backend.app.db.db import init_db, log_query

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

    log_query(
        req.query,
        req.top_k,
        req.alpha,
        len(results)
    )

    return {"results": results}