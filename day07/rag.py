from dotenv import load_dotenv
from openai import OpenAI

from day07.semantic_search import retrieve


load_dotenv()

client = OpenAI()


def build_context(results):

    context_parts = []

    for item in results:

        chunk_id = item["chunk_id"]
        text = item["text"]

        context_parts.append(
            f"[Chunk {chunk_id}]\n{text}"
        )

    return "\n\n".join(context_parts)


def answer_question(question, top_k=3):

    # 1. 检索相关文档
    results = retrieve(
        question,
        top_k=top_k
    )

    # 2. 构建上下文
    context = build_context(results)

    # 3. 调用 LLM
    response = client.responses.create(
        model="gpt-4.1-mini",

        instructions="""
You are an RWA research assistant.

Answer the user's question using only the
provided reference documents.

Rules:
1. Do not invent facts.
2. If the documents do not contain enough
   information, explicitly say so.
3. Cite the supporting Chunk IDs.
4. Distinguish clearly between what the
   documents state and what they do not establish.
5. Answer in the same language as the user.
""",

        input=f"""
Reference documents:

{context}

User question:
{question}
"""
    )

    return {
        "answer": response.output_text,
        "sources": results
    }


if __name__ == "__main__":

    while True:

        question = input(
            "\n请输入问题（exit退出）："
        ).strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        result = answer_question(question)

        print("\n===== AI Answer =====")
        print(result["answer"])

        print("\n===== Retrieved Sources =====")

        for source in result["sources"]:

            print(
                f"Chunk {source['chunk_id']} "
                f"| Score: {source['score']:.4f}"
            )