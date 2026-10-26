
from day17.schemas import (
    ResearchEvidence,
    ResearchQualityReport,
)

from day17.semantic_validator import (
    validate_semantically,
)

from day17.quality_scorer import (
    calculate_research_quality,
)


def run_quality_pipeline(
    evidence_list: list[ResearchEvidence],
    trusted_sources: dict[str, str],
) -> ResearchQualityReport:
    """
    Validate evidence and calculate quality metrics.

    Invalid sources remain unverified.
    Valid sources undergo semantic evaluation.
    """

    validated_evidence = []

    for evidence in evidence_list:

        validated, judgment = validate_semantically(
            evidence,
            trusted_sources,
        )

        print(
            f"Claim: {evidence.claim}"
        )

        print(
            f"Status: {validated.verification_status}"
        )

        if judgment is not None:
            print(
                f"Reason: {judgment.reasoning}"
            )

        print("-" * 50)

        validated_evidence.append(validated)

    report = calculate_research_quality(
        validated_evidence
    )

    return report
