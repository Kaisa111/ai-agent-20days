
from day17.claim_extractor import extract_tvl_claims

from day17.market_snapshot import (
    create_market_snapshot,
    build_snapshot_registry,
)

from day17.source_registry import (
    validate_registered_numeric_evidence,
)

from day17.quality_scorer import (
    calculate_research_quality,
)


protocols = [
    {
        "name": "Ethena USDtb",
        "tvl": 476796512.05,
    },
    {
        "name": "Huma",
        "tvl": 372955716.63,
    },
]

snapshot = create_market_snapshot(protocols)
registry = build_snapshot_registry(snapshot)


# Simulated LLM-generated research report
report_text = """
RWA Market Research Report

Ethena USDtb has a reported TVL of $476,796,512.05 USD.

Huma has a reported TVL of $3,729,557,166.30 USD.
"""


claims = extract_tvl_claims(
    report_text=report_text,
    snapshot_id=snapshot.snapshot_id,
    protocols=snapshot.protocols,
)

print("Extracted claims:", len(claims))

assert len(claims) == 2

validated = []

for claim in claims:
    result = validate_registered_numeric_evidence(
        claim,
        registry,
    )

    print(
        result.claim,
        "|",
        result.verification_status,
    )

    validated.append(result)


quality = calculate_research_quality(validated)

print("\nQUALITY REPORT")
print(quality.model_dump_json(indent=2))

assert quality.total_claims == 2
assert quality.verified_claims == 1
assert quality.contradicted_claims == 1
assert quality.evidence_coverage == 0.5

print("\nClaim extraction tests passed!")
