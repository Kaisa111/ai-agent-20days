
from day18.report_schemas import (
    ReportMetadata,
    ReportQuality,
    ResearchReport,
)
from day18.quality_gate import check_quality_gate


def make_report(
    verified: int,
    unverified: int,
    contradicted: int,
    completeness: float,
    status: str,
) -> ResearchReport:
    total = verified + unverified + contradicted

    return ResearchReport(
        metadata=ReportMetadata(
            title="Test Report",
            question="Test question",
            generated_at_utc="2026-10-27T00:00:00+00:00",
            snapshot_id="snapshot:test",
        ),
        executive_summary="Test summary",
        quality=ReportQuality(
            total_claims=total,
            verified_claims=verified,
            unverified_claims=unverified,
            contradicted_claims=contradicted,
            evidence_coverage=verified / total if total else 0.0,
            claim_completeness=completeness,
        ),
        overall_status=status,
    )


def main():
    good = make_report(
        verified=3,
        unverified=0,
        contradicted=0,
        completeness=1.0,
        status="verified",
    )

    good_result = check_quality_gate(good)
    print("Good report:", good_result)
    assert good_result.passed

    bad = make_report(
        verified=2,
        unverified=0,
        contradicted=1,
        completeness=1.0,
        status="requires_review",
    )

    bad_result = check_quality_gate(bad)
    print("Bad report:", bad_result)
    assert not bad_result.passed
    assert bad_result.reasons

    empty = make_report(
        verified=0,
        unverified=0,
        contradicted=0,
        completeness=0.0,
        status="partial",
    )

    empty_result = check_quality_gate(empty)
    print("Empty report:", empty_result)
    assert not empty_result.passed

    print("\nQuality gate tests passed!")


if __name__ == "__main__":
    main()
