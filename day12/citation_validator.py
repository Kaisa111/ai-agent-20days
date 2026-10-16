
import re


def extract_chunk_ids(text: str) -> set[int]:
    """
    Extract exact citations:
    [Chunk 4], [Chunk 6]
    """
    return {
        int(number)
        for number in re.findall(
            r"\[Chunk\s+(\d+)\]",
            text,
            flags=re.IGNORECASE,
        )
    }


def validate_citations(
    source_report: str,
    final_report: str,
) -> dict:

    source_ids = extract_chunk_ids(source_report)
    final_ids = extract_chunk_ids(final_report)

    unknown_ids = final_ids - source_ids
    missing_ids = source_ids - final_ids

    # Detect malformed or suspicious citations
    suspicious_patterns = [
        r"\[Crypto Agent[^\]]*Chunk[^\]]*\]",
        r"\[RWA Agent[^\]]*Chunk[^\]]*\]",
        r"\[Chunks?\s+\d+\s*[-–,]\s*\d+[^\]]*\]",
    ]

    suspicious_citations = []

    for pattern in suspicious_patterns:
        suspicious_citations.extend(
            re.findall(
                pattern,
                final_report,
                flags=re.IGNORECASE,
            )
        )

    has_valid_citations = len(final_ids) > 0

    citation_ids_valid = (
        has_valid_citations
        and len(unknown_ids) == 0
        and len(suspicious_citations) == 0
    )

    return {
        "source_citations": sorted(source_ids),
        "final_citations": sorted(final_ids),
        "unknown_citations": sorted(unknown_ids),
        "missing_citations": sorted(missing_ids),
        "suspicious_citations": suspicious_citations,
        "has_valid_citations": has_valid_citations,
        "citation_ids_valid": citation_ids_valid,
    }


if __name__ == "__main__":

    source = (
        "Liquidity risk [Chunk 4]. "
        "Legal ownership risk [Chunk 6]."
    )

    final = (
        "Liquidity risk [Chunk 4]. "
        "Bitcoin has high liquidity [Crypto Agent, Chunk 1–5]."
    )

    result = validate_citations(source, final)

    for key, value in result.items():
        print(f"{key}: {value}")
