
from datetime import datetime, timezone

from day17.schemas import ResearchEvidence

from day18.report_schemas import (
    ReportMetadata,
    ReportSection,
    ReportQuality,
    ResearchReport,
)


def build_research_report(
    question: str,
    pipeline_result: dict,
) -> ResearchReport:
    """
    Convert Day17 pipeline results
    into a structured Day18 report.
    """

    snapshot = pipeline_result["snapshot"]
    evidence = [
    item if isinstance(item, ResearchEvidence)
    else ResearchEvidence.model_validate(item)
    for item in pipeline_result["evidence"]
    ]
    from types import SimpleNamespace

    quality = SimpleNamespace(
        **pipeline_result["quality_report"]
    )

    coverage = SimpleNamespace(
        **pipeline_result["coverage_report"]
    )

    metadata = ReportMetadata(
        title="RWA Market Research Report",
        question=question,
        generated_at_utc=datetime.now(
            timezone.utc
        ).isoformat(),
        snapshot_id=snapshot["snapshot_id"],
    )

    verified_evidence = [
        item for item in evidence
        if item.verification_status == "verified"
    ]

    market_lines = []
    evidence_ids = []

    for item in verified_evidence:
        market_lines.append(f"- {item.claim}")
        evidence_ids.append(item.source_id)

    if not market_lines:
        market_lines.append(
            "No verified market claims are available."
        )

    sections = [
        ReportSection(
            title="Market Overview",
            content="\n".join(market_lines),
            evidence_ids=evidence_ids,
        )
    ]

    report_quality = ReportQuality(
        total_claims=quality.total_claims,
        verified_claims=quality.verified_claims,
        unverified_claims=quality.unverified_claims,
        contradicted_claims=quality.contradicted_claims,
        evidence_coverage=quality.evidence_coverage,
        claim_completeness=coverage.claim_completeness,
    )

    if (
        quality.contradicted_claims > 0
        or coverage.unknown_protocols
        or coverage.duplicate_protocols
    ):
        status = "requires_review"
    elif (
        quality.total_claims > 0
        and quality.evidence_coverage == 1.0
        and coverage.claim_completeness == 1.0
    ):
        status = "verified"
    else:
        status = "partial"

    summary = (
        f"Analyzed {quality.total_claims} claims. "
        f"{quality.verified_claims} were verified "
        f"against the selected data snapshot. "
        f"Claim completeness: "
        f"{coverage.claim_completeness:.0%}."
    )

    return ResearchReport(
        metadata=metadata,
        executive_summary=summary,
        sections=sections,
        quality=report_quality,
        limitations=[
            "TVL does not equal total tokenized RWA issuance.",
            "Verification checks consistency with one API snapshot.",
            "The selected protocols may not represent the entire RWA market.",
            "Credit, liquidity, legal and smart-contract risks "
            "have not yet been independently assessed.",
        ],
        overall_status=status,
    )
