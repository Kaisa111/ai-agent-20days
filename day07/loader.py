def load_document(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        text = file.read()

    return text


def split_into_chunks(text):
    chunks = text.split("\n\n")

    clean_chunks = []

    for chunk in chunks:
        chunk = chunk.strip()

        if chunk:
            clean_chunks.append(chunk)

    return clean_chunks


if __name__ == "__main__":
    document = load_document(
        "day07/data/rwa_intro.txt"
    )

    chunks = split_into_chunks(document)

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n===== Chunk {index} =====")
        print(chunk)