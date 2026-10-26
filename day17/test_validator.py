
from day17.schemas import ResearchEvidence
from day17.evidence_validator import validate_evidence


trusted_sources = {
    "Chunk 4": (
        "Liquidity risk occurs when investors "
        "cannot easily buy or sell the tokenized asset."
    )
}


def test_valid_evidence():
    evidence = ResearchEvidence(
        claim=trusted_sources["Chunk 4"],
        source_type="knowledge_base",
        source_id="Chunk 4",
        evidence_text=trusted_sources["Chunk 4"],
    )

    result = validate_evidence(
        evidence,
        trusted_sources,
    )

    print("Valid evidence:", result.verification_status)


def test_invalid_source():
    evidence = ResearchEvidence(
        claim="RWA investments involve liquidity risk",
        source_type="knowledge_base",
        source_id="Chunk 999",
        evidence_text="Liquidity risk exists.",
    )

    result = validate_evidence(
        evidence,
        trusted_sources,
    )

    print("Invalid source:", result.verification_status)


def test_contradictory_evidence():
    source_text = (
        "RWA investments involve liquidity risk."
    )

    evidence = ResearchEvidence(
        claim=(
            "RWA investments do not involve "
            "liquidity risk."
        ),
        source_type="knowledge_base",
        source_id="Chunk 10",
        evidence_text=source_text,
    )

    result = validate_evidence(
        evidence,
        {"Chunk 10": source_text},
    )

    print(
        "Contradictory evidence:",
        result.verification_status,
    )

    assert result.verification_status != "verified", (
        "Contradictory claim was incorrectly verified!"
    )


if __name__ == "__main__":
    test_valid_evidence()
    test_invalid_source()
    test_contradictory_evidence()
