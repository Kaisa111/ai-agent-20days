from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def rewrite_query(question: str) -> str:

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions="""
You are a search query optimization assistant
for a Real World Asset (RWA) knowledge base.

Rewrite the user's question to improve
semantic retrieval.

Rules:
1. Preserve the user's original intent.
2. Use precise financial or blockchain terminology
   when appropriate.
3. Do not answer the question.
4. Do not invent facts or assume a specific answer.
5. Return only one rewritten search query.
6. Keep the same language as the original question.
""",
        input=question
    )

    rewritten = response.output_text.strip()

    return rewritten if rewritten else question