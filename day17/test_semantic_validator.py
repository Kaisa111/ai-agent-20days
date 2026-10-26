
from day17.schemas import ResearchEvidence
from day17.semantic_validator import validate_semantically


source_text = (
    "Liquidity risk occurs when investors "
    "cannot easily buy or sell the tokenized asset."
)

trusted_sources = {
    "Chunk 4": source_text,
}


test_cases = [
    (
        "Tokenized assets may be difficult to sell.",
        "supported",
    ),
    (
        "Tokenized assets can always be sold easily.",
        "contradicted",
    ),
    (
        "Tokenized assets guarantee a 15% annual return.",
        "insufficient",
    ),
]


for claim, expected in test_cases:
    evidence = ResearchEvidence(
        claim=claim,
        source_type="knowledge_base",
        source_id="Chunk 4",
        evidence_text=source_text,
    )

    result, judgment = validate_semantically(
        evidence,
        trusted_sources,
    )

    print("\nClaim:", claim)
    print("Expected:", expected)
    print("Actual:", judgment.relationship)
    print("Reason:", judgment.reasoning)

    assert judgment.relationship == expected

print("\nAll semantic validation tests passed!")
