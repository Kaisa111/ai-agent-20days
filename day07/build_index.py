import json

from day07.loader import (
    load_document,
    split_into_chunks
)

from day07.semantic_search import get_embeddings


def build_index():

    document = load_document(
        "day07/data/rwa_intro.txt"
    )

    chunks = split_into_chunks(document)

    embeddings = get_embeddings(chunks)

    index = []

    for i, (chunk, embedding) in enumerate(
        zip(chunks, embeddings),
        start=1
    ):
        index.append({
            "chunk_id": i,
            "text": chunk,
            "embedding": embedding
        })

    with open(
        "day07/data/vector_index.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            index,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Index built successfully: "
        f"{len(index)} chunks"
    )


if __name__ == "__main__":
    build_index()