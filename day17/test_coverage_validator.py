
from day17.llm_claim_generator import TVLClaim

from day17.coverage_validator import (
    validate_claim_coverage,
)


protocols = [
    {"name": "Ethena USDtb"},
    {"name": "Re"},
    {"name": "Huma"},
]


def make_claim(name):
    return TVLClaim(
        protocol_name=name,
        reported_tvl_usd=100.0,
    )


# Case 1: All protocols covered
complete = validate_claim_coverage(
    protocols,
    [
        make_claim("Ethena USDtb"),
        make_claim("Re"),
        make_claim("Huma"),
    ],
)

print(
    "Complete:",
    complete.claim_completeness
)

assert complete.claim_completeness == 1.0


# Case 2: One protocol missing
missing = validate_claim_coverage(
    protocols,
    [
        make_claim("Ethena USDtb"),
        make_claim("Re"),
    ],
)

print(
    "Missing:",
    missing.missing_protocols
)

assert missing.missing_protocols == ["Huma"]
assert missing.claim_completeness == 0.6667


# Case 3: Duplicate and invented protocol
invalid = validate_claim_coverage(
    protocols,
    [
        make_claim("Ethena USDtb"),
        make_claim("Ethena USDtb"),
        make_claim("Re"),
        make_claim("Fake Protocol"),
    ],
)

print(
    "Duplicates:",
    invalid.duplicate_protocols
)
print(
    "Unknown:",
    invalid.unknown_protocols
)

assert invalid.duplicate_protocols == [
    "Ethena USDtb"
]
assert invalid.unknown_protocols == [
    "Fake Protocol"
]
assert invalid.claim_completeness == 0.3333


print("\nCoverage validation tests passed!")
