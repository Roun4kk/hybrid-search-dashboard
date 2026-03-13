import json
import csv
import datetime
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

    queries = [json.loads(line) for line in open("data/eval/queries.jsonl")]
    qrels = json.load(open("data/eval/qrels.json"))

    ndcg_scores = []
    recall_scores = []
    mrr_scores = []

    for q in queries:

        query = q["query"]
        qid = q["query_id"]

        relevant = qrels.get(qid, [])

        results = search.search(query, top_k=10)

        ndcg_scores.append(ndcg_at_k(results, relevant))
        recall_scores.append(recall_at_k(results, relevant))
        mrr_scores.append(mrr(results, relevant))

    avg_ndcg = sum(ndcg_scores) / len(ndcg_scores)
    avg_recall = sum(recall_scores) / len(recall_scores)
    avg_mrr = sum(mrr_scores) / len(mrr_scores)

    print("Average nDCG:", avg_ndcg)
    print("Average Recall:", avg_recall)
    print("Average MRR:", avg_mrr)

    # save experiment
    with open("data/metrics/experiments.csv", "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            datetime.datetime.now(),
            0.5,
            avg_ndcg,
            avg_recall,
            avg_mrr
        ])


if __name__ == "__main__":
    run_eval()