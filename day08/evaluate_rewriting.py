import json

from day07.semantic_search import retrieve
from day08.query_rewriter import rewrite_query


def reciprocal_rank(retrieved_ids, relevant_ids):

    relevant = set(relevant_ids)

    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant:
            return 1 / rank

    return 0.0


def evaluate_query(query, relevant_ids):

    results = retrieve(query, top_k=3)

    retrieved_ids = [
        item["chunk_id"]
        for item in results
    ]

    relevant = set(relevant_ids)

    return {
        "recall_1": len(
            set(retrieved_ids[:1]) & relevant
        ) / len(relevant),

        "recall_2": len(
            set(retrieved_ids[:2]) & relevant
        ) / len(relevant),

        "recall_3": len(
            set(retrieved_ids[:3]) & relevant
        ) / len(relevant),

        "mrr_3": reciprocal_rank(
            retrieved_ids,
            relevant_ids
        ),

        "retrieved_ids": retrieved_ids
    }


def average_metrics(results):

    metric_names = [
        "recall_1",
        "recall_2",
        "recall_3",
        "mrr_3"
    ]

    return {
        name: sum(
            result[name] for result in results
        ) / len(results)
        for name in metric_names
    }


def main():

    with open(
        "day08/eval_dataset.json",
        "r",
        encoding="utf-8"
    ) as file:
        dataset = json.load(file)

    original_results = []
    rewritten_results = []

    for sample in dataset:

        question = sample["question"]
        relevant_ids = sample["relevant_chunk_ids"]

        rewritten_query = rewrite_query(question)

        original = evaluate_query(
            question,
            relevant_ids
        )

        rewritten = evaluate_query(
            rewritten_query,
            relevant_ids
        )

        original_results.append(original)
        rewritten_results.append(rewritten)

        print(f"\n===== Q{sample['id']} =====")
        print(f"Original: {question}")
        print(f"Rewritten: {rewritten_query}")

        print(
            "Original Top3:",
            original["retrieved_ids"]
        )

        print(
            "Rewritten Top3:",
            rewritten["retrieved_ids"]
        )

    original_avg = average_metrics(original_results)
    rewritten_avg = average_metrics(rewritten_results)

    print("\n========== FINAL COMPARISON ==========")

    for name in original_avg:

        print(
            f"{name}: "
            f"Original={original_avg[name]:.2%} | "
            f"Rewritten={rewritten_avg[name]:.2%}"
        )


if __name__ == "__main__":
    main()