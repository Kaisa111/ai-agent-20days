from day07.semantic_search import retrieve


question = (
    "Why might it be difficult "
    "to exit an RWA investment?"
)

results = retrieve(
    question,
    top_k=6
)

print(f"\nQuestion: {question}")

for rank, item in enumerate(results, start=1):

    print(
        f"\nRank {rank}"
        f" | Chunk {item['chunk_id']}"
        f" | Score {item['score']:.4f}"
    )

    print(item["text"])