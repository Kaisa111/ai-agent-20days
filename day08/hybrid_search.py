from day07.semantic_search import retrieve
from day08.bm25_search import bm25_retrieve


def hybrid_retrieve(question, top_k=3, rrf_k=60):

    # 获取两个检索器的完整候选排名
    semantic_results = retrieve(question, top_k=6)
    bm25_results = bm25_retrieve(question, top_k=6)

    scores = {}
    documents = {}

    for results in [semantic_results, bm25_results]:

        for rank, item in enumerate(results, start=1):

            chunk_id = item["chunk_id"]

            scores[chunk_id] = (
                scores.get(chunk_id, 0)
                + 1 / (rrf_k + rank)
            )

            documents[chunk_id] = item["text"]

    fused_results = []

    for chunk_id, score in scores.items():

        fused_results.append({
            "chunk_id": chunk_id,
            "text": documents[chunk_id],
            "score": score
        })

    fused_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return fused_results[:top_k]


if __name__ == "__main__":

    question = (
        "Why might it be difficult "
        "to exit an RWA investment?"
    )

    results = hybrid_retrieve(question, top_k=6)

    print(f"\nQuestion: {question}")

    for rank, item in enumerate(results, start=1):

        print(
            f"Rank {rank} | "
            f"Chunk {item['chunk_id']} | "
            f"RRF Score {item['score']:.6f}"
        )