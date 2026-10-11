import re

from rank_bm25 import BM25Okapi
from day07.loader import load_document, split_into_chunks


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


text = load_document("day07/data/rwa_intro.txt")
chunks = split_into_chunks(text)

tokenized_chunks = [
    tokenize(chunk)
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_chunks)


def bm25_retrieve(question, top_k=3):

    query_tokens = tokenize(question)

    scores = bm25.get_scores(query_tokens)

    results = []

    for i, score in enumerate(scores):

        # 检查文档是否包含查询中的任意词
        matched_tokens = (
            set(query_tokens)
            & set(tokenized_chunks[i])
        )

        if not matched_tokens:
            continue

        results.append({
            "chunk_id": i + 1,
            "text": chunks[i],
            "score": float(score)
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    question = (
        "Why might it be difficult "
        "to exit an RWA investment?"
    )

    results = bm25_retrieve(question, top_k=6)

    print(f"\nQuestion: {question}")

    for rank, item in enumerate(results, start=1):

        print(
            f"Rank {rank} | "
            f"Chunk {item['chunk_id']} | "
            f"BM25 Score {item['score']:.4f}"
        )