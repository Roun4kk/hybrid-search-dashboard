from backend.app.search.bm25 import BM25Index
from backend.app.search.vector import VectorIndex


class HybridSearch:

    def __init__(self):

        self.bm25 = BM25Index()
        self.vector = VectorIndex()

        self.bm25.load("data/index/bm25")
        self.vector.load("data/index/vector")

    def normalize(self, scores):

        if not scores:
            return []

        min_s = min(scores)
        max_s = max(scores)

        if max_s - min_s == 0:
            return [0 for _ in scores]

        return [(s - min_s) / (max_s - min_s) for s in scores]

    def search(self, query, top_k=5, alpha=0.5):

        bm25_results = self.bm25.search(query, top_k)
        vector_results = self.vector.search(query, top_k)

        bm25_scores = [r["score"] for r in bm25_results]
        vector_scores = [r["score"] for r in vector_results]

        bm25_norm = self.normalize(bm25_scores)
        vector_norm = self.normalize(vector_scores)

        results = []

        for i in range(len(bm25_results)):

            hybrid_score = (
                alpha * bm25_norm[i]
                + (1 - alpha) * vector_norm[i]
            )

            results.append({
                "doc_id": bm25_results[i]["doc_id"],
                "title": bm25_results[i]["title"],
                "bm25_score": bm25_scores[i],
                "vector_score": vector_scores[i],
                "hybrid_score": hybrid_score
            })

        results.sort(
            key=lambda x: x["hybrid_score"],
            reverse=True
        )

        return results