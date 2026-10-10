import json
import math

from dotenv import load_dotenv
from openai import OpenAI

from day07.loader import (
    load_document,
    split_into_chunks
)

from day07.retriever import rank_chunks


load_dotenv()

client = OpenAI()


def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def get_embeddings(texts):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [
        item.embedding
        for item in response.data
    ]


def retrieve(question, top_k=2):

    # 1. 加载本地向量索引
    with open(
        "day07/data/vector_index.json",
        "r",
        encoding="utf-8"
    ) as file:

        index = json.load(file)

    # 2. 只生成用户问题的向量
    question_embedding = get_embeddings(
        [question]
    )[0]

    # 3. 计算问题与每个Chunk的相似度
    results = []

    for item in index:

        score = cosine_similarity(
            question_embedding,
            item["embedding"]
        )

        results.append({
            "chunk_id": item["chunk_id"],
            "text": item["text"],
            "score": score
        })

    # 4. 按相似度降序排列
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # 5. 返回Top-K
    return results[:top_k]


if __name__ == "__main__":

    while True:

        question = input(
            "\n请输入问题（输入exit退出）："
        ).strip()

        if question.lower() == "exit":
            print("程序结束")
            break

        if not question:
            continue

        results = retrieve(
            question,
            top_k=2
        )

        for result in results:

            print(
                f"\nChunk {result['chunk_id']} "
                f"| Similarity: {result['score']:.4f}"
            )

            print(result["text"])