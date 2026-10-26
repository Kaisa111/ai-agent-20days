
from day17.schemas import ResearchEvidence
from day17.numeric_validator import (
    validate_numeric_evidence,
)


protocol = {
    "name": "Protocol A",
    "tvl": 125000000.0,
}


def make_evidence(claim: str):
    return ResearchEvidence(
        claim=claim,
        source_type="api",
        source_id="DefiLlama:protocol:1",
        evidence_text=(
            "Protocol: Protocol A; "
            "TVL_USD: 125,000,000.00; "
            "Source: DefiLlama"
        ),
    )


# Case 1: Correct TVL
correct = make_evidence(
    "Protocol A has a reported TVL "
    "of $125,000,000.00 USD."
)

result = validate_numeric_evidence(
    correct, protocol
)

print("Correct TVL:", result.verification_status)
assert result.verification_status == "verified"


# Case 2: Incorrect TVL (10x)
incorrect = make_evidence(
    "Protocol A has a reported TVL "
    "of $1,250,000,000.00 USD."
)

result = validate_numeric_evidence(
    incorrect, protocol
)

print("Incorrect TVL:", result.verification_status)
assert result.verification_status == "contradicted"


# Case 3: Unrecognized claim format
unknown = make_evidence(
    "Protocol A is the safest RWA investment."
)

result = validate_numeric_evidence(
    unknown, protocol
)

print("Unknown claim:", result.verification_status)
assert result.verification_status == "unverified"


print("\nNumeric validation tests passed!")
