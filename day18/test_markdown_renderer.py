
from day18.report_schemas import (
    ReportMetadata,
    ReportSection,
    ReportQuality,
    ResearchReport,
)

from day18.markdown_renderer import render_markdown


def main():
    report = ResearchReport(
        metadata=ReportMetadata(
            title="RWA Market Research Report",
            question="目前主要RWA协议的TVL是多少？",
            generated_at_utc="2026-10-27T00:00:00+00:00",
            snapshot_id="snapshot:test123",
        ),
        executive_summary=(
            "This report analyzes selected "
            "RWA protocols and their TVL."
        ),
        sections=[
            ReportSection(
                title="Market Overview",
                content=(
                    "Ethena USDtb has a reported TVL "
                    "of $476,810,438.39 USD."
                ),
                evidence_ids=[
                    "snapshot:test123:protocol-a"
                ],
            ),
            ReportSection(
                title="Risk Analysis",
                content=(
                    "RWA protocols may involve "
                    "liquidity, credit, and legal risks."
                ),
            ),
        ],
        quality=ReportQuality(
            total_claims=3,
            verified_claims=3,
            evidence_coverage=1.0,
            claim_completeness=1.0,
        ),
        limitations=[
            "TVL does not equal total RWA issuance.",
            "Data represents a specific API snapshot.",
        ],
        overall_status="verified",
    )

    markdown = render_markdown(report)

    print(markdown)

    assert "# RWA Market Research Report" in markdown
    assert "## Executive Summary" in markdown
    assert "## Market Overview" in markdown
    assert "## Risk Analysis" in markdown
    assert "## Research Quality" in markdown
    assert "## Limitations" in markdown
    assert "100.00%" in markdown

    print("\nMarkdown renderer tests passed!")


if __name__ == "__main__":
    main()
