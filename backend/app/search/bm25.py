import json
import os
import pickle
from rank_bm25 import BM25Okapi


class BM25Index:

    def __init__(self):
        self.bm25 = None
        self.documents = []
        self.tokenized_corpus = []

    def build(self, docs_path):
        docs = []

        with open(docs_path, "r", encoding="utf-8") as f:
            for line in f:
                docs.append(json.loads(line))

        corpus = []

        for doc in docs:
            text = (doc["title"] + " " + doc["text"]).lower()
            tokens = text.split()
            corpus.append(tokens)

        self.tokenized_corpus = corpus
        self.documents = docs

        self.bm25 = BM25Okapi(corpus)

    def save(self, out_dir):
        os.makedirs(out_dir, exist_ok=True)

        with open(os.path.join(out_dir, "bm25.pkl"), "wb") as f:
            pickle.dump({
                "bm25": self.bm25,
                "docs": self.documents,
                "corpus": self.tokenized_corpus
            }, f)

    def load(self, index_dir):

        with open(os.path.join(index_dir, "bm25.pkl"), "rb") as f:
            data = pickle.load(f)

        self.bm25 = data["bm25"]
        self.documents = data["docs"]
        self.tokenized_corpus = data["corpus"]

    def search(self, query, top_k=5):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []

        for idx, score in ranked:
            doc = self.documents[idx]

            results.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "score": float(score)
            })

        return results