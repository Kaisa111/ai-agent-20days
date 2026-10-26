
from dataclasses import dataclass, field

from day18.report_schemas import ResearchReport


@dataclass
class GateResult:
    passed: bool
    reasons: list[str] = field(default_factory=list)


def check_quality_gate(
    report: ResearchReport,
    min_evidence_coverage: float = 1.0,
    min_claim_completeness: float = 1.0,
) -> GateResult:
    """
    Decide whether a report meets the
    minimum requirements for publication.
    """

    reasons = []
    quality = report.quality

    if report.overall_status != "verified":
        reasons.append(
            f"Report status is {report.overall_status}."
        )

    if quality.total_claims == 0:
        reasons.append("No research claims were evaluated.")

    if quality.contradicted_claims > 0:
        reasons.append(
            f"{quality.contradicted_claims} contradicted claims."
        )

    if quality.unverified_claims > 0:
        reasons.append(
            f"{quality.unverified_claims} unverified claims."
        )

    if quality.evidence_coverage < min_evidence_coverage:
        reasons.append(
            "Evidence coverage below required threshold."
        )

    if quality.claim_completeness < min_claim_completeness:
        reasons.append(
            "Claim completeness below required threshold."
        )

    return GateResult(
        passed=len(reasons) == 0,
        reasons=reasons,
    )
