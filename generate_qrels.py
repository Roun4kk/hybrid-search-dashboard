import json
from backend.app.search.hybrid import HybridSearch

search = HybridSearch()

# load queries
queries = [json.loads(l) for l in open("data/eval/queries.jsonl")]

qrels = {}

for q in queries:
    qid = q["query_id"]
    query = q["query"]

    results = search.search(query, top_k=3)

    qrels[qid] = [r["doc_id"] for r in results]

with open("data/eval/qrels.json", "w") as f:
    json.dump(qrels, f, indent=2)

print("Generated qrels for", len(qrels), "queries")