from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.search.hybrid import HybridSearch

app = FastAPI(title="Hybrid Search + KPI Dashboard", version="1.0")

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

    return {"results": results}