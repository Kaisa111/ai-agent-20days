
from datetime import datetime, timezone

from day18.report_schemas import (
    ReportMetadata,
    ReportSection,
    ReportQuality,
    ResearchReport,
)


def main():
    metadata = ReportMetadata(
        title="RWA Market Research Report",
        question="目前主要RWA协议的TVL是多少？",
        generated_at_utc=datetime.now(
            timezone.utc
        ).isoformat(),
        snapshot_id="snapshot:test123",
    )

    market_section = ReportSection(
        title="Market Overview",
        content=(
            "The report summarizes TVL data "
            "from selected RWA protocols."
        ),
        evidence_ids=[
            "snapshot:test123:protocol-a"
        ],
    )

    quality = ReportQuality(
        total_claims=3,
        verified_claims=3,
        evidence_coverage=1.0,
        claim_completeness=1.0,
    )

    report = ResearchReport(
        metadata=metadata,
        executive_summary=(
            "This report reviews selected "
            "RWA protocol market data."
        ),
        sections=[market_section],
        quality=quality,
        limitations=[
            "TVL does not represent total RWA issuance.",
            "Data reflects a specific API snapshot.",
        ],
        overall_status="verified",
    )

    print(report.model_dump_json(indent=2))

    assert report.metadata.title == (
        "RWA Market Research Report"
    )

    assert len(report.sections) == 1
    assert report.quality.verified_claims == 3
    assert report.overall_status == "verified"

    print("\nReport schema tests passed!")


if __name__ == "__main__":
    main()
