import json
import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class VectorIndex:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = None

    def build(self, docs_path):

        docs = []
        texts = []

        with open(docs_path, "r", encoding="utf-8") as f:
            for line in f:
                doc = json.loads(line)
                docs.append(doc)
                texts.append(doc["title"] + " " + doc["text"])

        embeddings = self.model.encode(texts)

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype("float32"))

        self.documents = docs

    def save(self, out_dir):

        os.makedirs(out_dir, exist_ok=True)

        faiss.write_index(self.index, os.path.join(out_dir, "vector.index"))

        with open(os.path.join(out_dir, "vector_docs.pkl"), "wb") as f:
            pickle.dump(self.documents, f)

    def load(self, index_dir):

        self.index = faiss.read_index(os.path.join(index_dir, "vector.index"))

        with open(os.path.join(index_dir, "vector_docs.pkl"), "rb") as f:
            self.documents = pickle.load(f)

    def search(self, query, top_k=5):

        embedding = self.model.encode([query])

        D, I = self.index.search(np.array(embedding).astype("float32"), top_k)

        results = []

        for idx, score in zip(I[0], D[0]):
            doc = self.documents[idx]

            results.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "score": float(score)
            })

        return results