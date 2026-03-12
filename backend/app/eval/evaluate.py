import math
from backend.app.search.hybrid import HybridSearch


def dcg(relevances):
    score = 0
    for i, rel in enumerate(relevances):
        score += rel / math.log2(i + 2)
    return score


def ndcg_at_k(results, relevant_docs, k=10):
    relevances = []

    for r in results[:k]:
        if r["doc_id"] in relevant_docs:
            relevances.append(1)
        else:
            relevances.append(0)

    ideal = sorted(relevances, reverse=True)

    if sum(ideal) == 0:
        return 0

    return dcg(relevances) / dcg(ideal)


def recall_at_k(results, relevant_docs, k=10):
    retrieved = set([r["doc_id"] for r in results[:k]])
    relevant = set(relevant_docs)

    if len(relevant) == 0:
        return 0

    return len(retrieved & relevant) / len(relevant)


def mrr(results, relevant_docs):
    for i, r in enumerate(results):
        if r["doc_id"] in relevant_docs:
            return 1 / (i + 1)
    return 0


def run_eval():

    search = HybridSearch()

    queries = [
        ("machine learning", ["doc1.txt"]),
        ("python programming", ["doc2.txt"]),
        ("api framework", ["doc3.txt"])
    ]

    ndcg_scores = []
    recall_scores = []
    mrr_scores = []

    for query, relevant in queries:

        results = search.search(query, top_k=10)

        ndcg_scores.append(ndcg_at_k(results, relevant))
        recall_scores.append(recall_at_k(results, relevant))
        mrr_scores.append(mrr(results, relevant))

    print("Average nDCG:", sum(ndcg_scores) / len(ndcg_scores))
    print("Average Recall:", sum(recall_scores) / len(recall_scores))
    print("Average MRR:", sum(mrr_scores) / len(mrr_scores))


if __name__ == "__main__":
    run_eval()