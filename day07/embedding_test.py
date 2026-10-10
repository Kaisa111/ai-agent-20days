import math
import os

from dotenv import load_dotenv
from openai import OpenAI

from day07.loader import (
    load_document,
    split_into_chunks
)


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


document = load_document(
    "day07/data/rwa_intro.txt"
)

chunks = split_into_chunks(document)


response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)


print(f"Number of chunks: {len(chunks)}")
print(f"Number of embeddings: {len(response.data)}")

first_embedding = response.data[0].embedding

print(f"Vector dimensions: {len(first_embedding)}")
print(f"First 10 numbers: {first_embedding[:10]}")

question = "Can investors easily sell the token?"


question_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)


question_embedding = (
    question_response.data[0].embedding
)


print(
    f"Question vector dimensions: "
    f"{len(question_embedding)}"
)

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

    return dot_product / (
        magnitude_a * magnitude_b
    )

for index, item in enumerate(
    response.data,
    start=1
):
    chunk_embedding = item.embedding

    score = cosine_similarity(
        question_embedding,
        chunk_embedding
    )

    print(
        f"Chunk {index}: "
        f"{score:.4f}"
    )