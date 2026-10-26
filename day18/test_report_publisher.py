
from pathlib import Path
from tempfile import TemporaryDirectory

from day18.report_schemas import (
    ReportMetadata,
    ReportQuality,
    ResearchReport,
)

from day18.report_publisher import publish_report


def make_report(
    verified: int,
    contradicted: int,
    status: str,
) -> ResearchReport:
    total = verified + contradicted

    return ResearchReport(
        metadata=ReportMetadata(
            title="RWA Test Report",
            question="What is the RWA market TVL?",
            generated_at_utc="2026-10-27T00:00:00+00:00",
            snapshot_id="snapshot:test",
        ),
        executive_summary="Test report.",
        quality=ReportQuality(
            total_claims=total,
            verified_claims=verified,
            contradicted_claims=contradicted,
            evidence_coverage=(
                verified / total if total else 0.0
            ),
            claim_completeness=1.0,
        ),
        overall_status=status,
    )


def main():
    with TemporaryDirectory() as temp_dir:
        good_report = make_report(
            verified=3,
            contradicted=0,
            status="verified",
        )

        good_result = publish_report(
            good_report,
            output_dir=temp_dir,
        )

        print("Good report:", good_result)

        assert good_result.published
        assert Path(good_result.file_path).exists()
        assert Path(good_result.file_path).parent.name == "published"

        bad_report = make_report(
            verified=2,
            contradicted=1,
            status="requires_review",
        )

        bad_result = publish_report(
            bad_report,
            output_dir=temp_dir,
        )

        print("Bad report:", bad_result)

        assert not bad_result.published
        assert Path(bad_result.file_path).exists()
        assert Path(bad_result.file_path).parent.name == "review"

        content = Path(
            bad_result.file_path
        ).read_text(encoding="utf-8")

        assert "REQUIRES REVIEW" in content
        assert "contradicted claims" in content

    print("\nReport publisher tests passed!")


if __name__ == "__main__":
    main()
