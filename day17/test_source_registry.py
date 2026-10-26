
from day17.schemas import ResearchEvidence

from day17.source_registry import (
    build_source_registry,
    create_source_id,
    validate_registered_numeric_evidence,
)


protocols = [
    {
        "name": "Protocol A",
        "slug": "protocol-a",
        "tvl": 125000000.0,
    },
    {
        "name": "Protocol B",
        "slug": "protocol-b",
        "tvl": 85000000.0,
    },
]

registry = build_source_registry(protocols)

print("Registered sources:", len(registry))

source_id = create_source_id(protocols[0])

correct = ResearchEvidence(
    claim=(
        "Protocol A has a reported TVL "
        "of $125,000,000.00 USD."
    ),
    source_type="api",
    source_id=source_id,
    evidence_text=(
        "Protocol: Protocol A; "
        "TVL_USD: 125,000,000.00; "
        "Source: DefiLlama"
    ),
)

result = validate_registered_numeric_evidence(
    correct,
    registry,
)

print("Correct source:", result.verification_status)
assert result.verification_status == "verified"


# Same claim, but pointing to another protocol
wrong_source = correct.model_copy(deep=True)
wrong_source.source_id = create_source_id(protocols[1])

result = validate_registered_numeric_evidence(
    wrong_source,
    registry,
)

print("Wrong source:", result.verification_status)
assert result.verification_status != "verified"


# Source does not exist
missing_source = correct.model_copy(deep=True)
missing_source.source_id = "DefiLlama:protocol:missing"

result = validate_registered_numeric_evidence(
    missing_source,
    registry,
)

print("Missing source:", result.verification_status)
assert result.verification_status == "unverified"


print("\nSource registry tests passed!")
