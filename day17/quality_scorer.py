
from day17.schemas import (
    ResearchEvidence,
    ResearchQualityReport,
)


def calculate_research_quality(
    evidence_list: list[ResearchEvidence],
) -> ResearchQualityReport:
    """
    Calculate research evidence quality metrics.

    One evidence item represents one claim.
    'verified' means source-supported, not
    independently fact-checked.
    """

    total = len(evidence_list)

    verified = sum(
        e.verification_status == "verified"
        for e in evidence_list
    )

    unverified = sum(
        e.verification_status == "unverified"
        for e in evidence_list
    )

    contradicted = sum(
        e.verification_status == "contradicted"
        for e in evidence_list
    )

    coverage = (
        round(verified / total, 4)
        if total > 0
        else 0.0
    )

    return ResearchQualityReport(
        total_claims=total,
        verified_claims=verified,
        unverified_claims=unverified,
        contradicted_claims=contradicted,
        evidence_coverage=coverage,
    )
