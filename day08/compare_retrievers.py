import json

from day07.semantic_search import retrieve
from day08.bm25_search import bm25_retrieve
from day08.hybrid_search import hybrid_retrieve


def calculate_metrics(retrieved_ids, relevant_ids):

    relevant = set(relevant_ids)

    metrics = {}

    for k in [1, 2, 3]:

        top_k_ids = set(retrieved_ids[:k])

        matched = top_k_ids & relevant

        metrics[f"recall_{k}"] = (
            len(matched) / len(relevant)
            if relevant else 0.0
        )

    reciprocal_rank = 0.0

    for rank, chunk_id in enumerate(
        retrieved_ids[:3],
        start=1
    ):

        if chunk_id in relevant:

            reciprocal_rank = 1 / rank
            break

    metrics["mrr_3"] = reciprocal_rank

    return metrics


def evaluate_retriever(name, retrieve_function, dataset):

    all_metrics = []

    print(f"\n===== {name} =====")

    for sample in dataset:

        results = retrieve_function(
            sample["question"],
            top_k=3
        )

        retrieved_ids = [
            item["chunk_id"]
            for item in results
        ]

        metrics = calculate_metrics(
            retrieved_ids,
            sample["relevant_chunk_ids"]
        )

        all_metrics.append(metrics)

        print(
            f"Q{sample['id']}: "
            f"Expected={sample['relevant_chunk_ids']} "
            f"Retrieved={retrieved_ids}"
        )

    metric_names = [
        "recall_1",
        "recall_2",
        "recall_3",
        "mrr_3"
    ]

    averages = {}

    for metric in metric_names:

        averages[metric] = sum(
            item[metric]
            for item in all_metrics
        ) / len(all_metrics)

    return averages


def main():

    with open(
        "day08/eval_dataset.json",
        "r",
        encoding="utf-8"
    ) as file:

        dataset = json.load(file)

    retrievers = {
        "Semantic": retrieve,
        "BM25": bm25_retrieve,
        "Hybrid": hybrid_retrieve
    }

    results = {}

    for name, retrieve_function in retrievers.items():

        results[name] = evaluate_retriever(
            name,
            retrieve_function,
            dataset
        )

    print("\n========== FINAL COMPARISON ==========")

    print(
        f"{'Retriever':<12}"
        f"{'Recall@1':<12}"
        f"{'Recall@2':<12}"
        f"{'Recall@3':<12}"
        f"{'MRR@3':<12}"
    )

    for name, metrics in results.items():

        print(
            f"{name:<12}"
            f"{metrics['recall_1']:<12.2%}"
            f"{metrics['recall_2']:<12.2%}"
            f"{metrics['recall_3']:<12.2%}"
            f"{metrics['mrr_3']:<12.2%}"
        )


if __name__ == "__main__":
    main()