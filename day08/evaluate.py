import json

from day07.semantic_search import retrieve


def recall_at_k(
    retrieved_ids,
    relevant_ids
):

    relevant = set(relevant_ids)
    retrieved = set(retrieved_ids)

    if not relevant:
        return 0.0

    matched = relevant.intersection(retrieved)

    return len(matched) / len(relevant)


def evaluate(k=1):

    with open(
        "day08/eval_dataset.json",
        "r",
        encoding="utf-8"
    ) as file:

        dataset = json.load(file)

    scores = []

    for sample in dataset:

        question = sample["question"]
        relevant_ids = sample["relevant_chunk_ids"]

        results = retrieve(
            question,
            top_k=k
        )

        retrieved_ids = [
            item["chunk_id"]
            for item in results
        ]

        score = recall_at_k(
            retrieved_ids,
            relevant_ids
        )

        scores.append(score)

        print(
            f"Question {sample['id']}: "
            f"Recall@{k} = {score:.2f}"
        )

        print(f"Expected: {relevant_ids}")
        print(f"Retrieved: {retrieved_ids}")
        print()

    average = sum(scores) / len(scores)

    print("=" * 40)

    print(
        f"Average Recall@{k}: "
        f"{average:.2%}"
    )


if __name__ == "__main__":

    for k in [1, 2, 3]:
        print(f"\n===== Evaluating Recall@{k} =====")
        evaluate(k=k)