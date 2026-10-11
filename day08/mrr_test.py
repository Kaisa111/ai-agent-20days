import json

from day07.semantic_search import retrieve


def reciprocal_rank(retrieved_ids, relevant_ids):

    relevant = set(relevant_ids)

    for rank, chunk_id in enumerate(
        retrieved_ids,
        start=1
    ):
        if chunk_id in relevant:
            return 1 / rank

    return 0.0


def evaluate_mrr(k=3):

    with open(
        "day08/eval_dataset.json",
        "r",
        encoding="utf-8"
    ) as file:
        dataset = json.load(file)

    rr_scores = []

    for sample in dataset:

        results = retrieve(
            sample["question"],
            top_k=k
        )

        retrieved_ids = [
            item["chunk_id"]
            for item in results
        ]

        rr = reciprocal_rank(
            retrieved_ids,
            sample["relevant_chunk_ids"]
        )

        rr_scores.append(rr)

        print(
            f"Q{sample['id']}: "
            f"Retrieved={retrieved_ids}, "
            f"RR={rr:.4f}"
        )

    mrr = sum(rr_scores) / len(rr_scores)

    print(f"\nMRR@{k}: {mrr:.2%}")


if __name__ == "__main__":
    evaluate_mrr(k=3)