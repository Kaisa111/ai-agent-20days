def rank_chunks(chunks, scores, top_k=2):

    results = []

    for index, (chunk, score) in enumerate(
        zip(chunks, scores),
        start=1
    ):
        results.append({
            "chunk_id": index,
            "text": chunk,
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]

if __name__ == "__main__":

    from day07.loader import (
        load_document,
        split_into_chunks
    )

    document = load_document(
        "day07/data/rwa_intro.txt"
    )

    chunks = split_into_chunks(document)

    scores = [
        0.2304,
        0.5274,
        0.2412,
        0.5726,
        0.3038,
        0.4117
    ]

    results = rank_chunks(
        chunks,
        scores,
        top_k=2
    )

    for result in results:
        print(
            f"\nChunk {result['chunk_id']} "
            f"| Score: {result['score']:.4f}"
        )
        print(result["text"])