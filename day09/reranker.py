import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from day08.hybrid_search import hybrid_retrieve


load_dotenv()
client = OpenAI()


class RerankResult(BaseModel):
    ranked_chunk_ids: list[int]


def rerank_documents(question, documents, top_k=3):

    if not documents:
        return []

    candidate_ids = {
        doc["chunk_id"] for doc in documents
    }

    context = "\n\n".join(
        f"Chunk {doc['chunk_id']}:\n{doc['text']}"
        for doc in documents
    )

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=(
            "You are a document relevance reranker. "
            "Rank the candidate chunks by how directly "
            "they answer the user's question. "
            "Prioritize specific evidence over broad topical similarity. "
            "Return the candidate chunk IDs in descending "
            "order of relevance. "
            "Use only IDs present in the candidates. "
            "Do not answer the question."
        ),
        input=(
            f"Question:\n{question}\n\n"
            f"Candidates:\n{context}"
        ),
        text_format=RerankResult
    )

    parsed = response.output_parsed

    if parsed is None:
        raise RuntimeError("Reranker returned no structured result")

    # 验证输出，防止无效 ID 或重复 ID
    ranked_ids = []
    seen = set()

    for chunk_id in parsed.ranked_chunk_ids:
        if chunk_id in candidate_ids and chunk_id not in seen:
            ranked_ids.append(chunk_id)
            seen.add(chunk_id)

    # 模型漏掉的候选保留原始检索顺序
    for doc in documents:
        chunk_id = doc["chunk_id"]

        if chunk_id not in seen:
            ranked_ids.append(chunk_id)
            seen.add(chunk_id)

    document_map = {
        doc["chunk_id"]: doc
        for doc in documents
    }

    return [
        document_map[chunk_id]
        for chunk_id in ranked_ids[:top_k]
    ]


if __name__ == "__main__":

    question = "What are the liquidity risks of RWA?"

    candidates = hybrid_retrieve(
        question,
        top_k=6
    )

    print("\nBefore Reranking:")

    for rank, doc in enumerate(candidates, start=1):
        print(f"Rank {rank}: Chunk {doc['chunk_id']}")

    reranked = rerank_documents(
        question,
        candidates,
        top_k=3
    )

    print("\nAfter Reranking:")

    for rank, doc in enumerate(reranked, start=1):
        print(f"Rank {rank}: Chunk {doc['chunk_id']}")