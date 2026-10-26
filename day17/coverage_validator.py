
from collections import Counter

from pydantic import BaseModel, Field


class CoverageReport(BaseModel):
    expected_protocols: int
    generated_claims: int

    covered_protocols: int
    missing_protocols: list[str] = Field(
        default_factory=list
    )
    duplicate_protocols: list[str] = Field(
        default_factory=list
    )
    unknown_protocols: list[str] = Field(
        default_factory=list
    )

    claim_completeness: float


def validate_claim_coverage(
    protocols: list[dict],
    claims: list,
) -> CoverageReport:
    """
    Check whether each source protocol has
    exactly one generated claim.

    Claims must expose a protocol_name field.
    """

    expected_names = [
        p["name"]
        for p in protocols
    ]

    if len(expected_names) != len(set(expected_names)):
        raise ValueError(
            "Duplicate protocol names in source data"
        )

    generated_names = [
        claim.protocol_name
        for claim in claims
    ]

    counts = Counter(generated_names)
    expected = set(expected_names)

    missing = [
        name
        for name in expected_names
        if counts[name] == 0
    ]

    duplicates = [
        name
        for name in expected_names
        if counts[name] > 1
    ]

    unknown = sorted(
        name
        for name in counts
        if name not in expected
    )

    # Only protocols represented exactly once count
    # as completely covered.
    covered = sum(
        counts[name] == 1
        for name in expected_names
    )

    total = len(expected_names)

    completeness = (
        round(covered / total, 4)
        if total
        else 0.0
    )

    return CoverageReport(
        expected_protocols=total,
        generated_claims=len(claims),
        covered_protocols=covered,
        missing_protocols=missing,
        duplicate_protocols=duplicates,
        unknown_protocols=unknown,
        claim_completeness=completeness,
    )
