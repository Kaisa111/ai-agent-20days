from day07.semantic_search import retrieve
from day08.query_rewriter import rewrite_query


question = (
    "Why might it be difficult "
    "to exit an RWA investment?"
)


def show_results(label, query):

    print(f"\n===== {label} =====")
    print(f"Query: {query}")

    results = retrieve(query, top_k=6)

    for rank, item in enumerate(results, start=1):

        print(
            f"Rank {rank} | "
            f"Chunk {item['chunk_id']} | "
            f"Score {item['score']:.4f}"
        )


if __name__ == "__main__":

    rewritten = rewrite_query(question)

    show_results(
        "Original Query",
        question
    )

    show_results(
        "AI Rewritten Query",
        rewritten
    )