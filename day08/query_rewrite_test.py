from day07.semantic_search import retrieve


original_query = (
    "Why might it be difficult "
    "to exit an RWA investment?"
)

rewritten_query = (
    "What liquidity risks make it difficult "
    "to sell or exit a tokenized asset position?"
)


def test_query(label, question):

    print(f"\n===== {label} =====")
    print(f"Question: {question}")

    results = retrieve(
        question,
        top_k=6
    )

    for rank, item in enumerate(results, start=1):

        print(
            f"Rank {rank} | "
            f"Chunk {item['chunk_id']} | "
            f"Score {item['score']:.4f}"
        )

        if item["chunk_id"] == 4:
            print(">>> Target Chunk 4 found here")


if __name__ == "__main__":

    test_query(
        "Original Query",
        original_query
    )

    test_query(
        "Rewritten Query",
        rewritten_query
    )