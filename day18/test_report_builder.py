
from day17.llm_quality_pipeline import (
    run_llm_quality_pipeline,
)

from day18.report_builder import build_research_report
from day18.markdown_renderer import render_markdown


def main():
    question = "目前主要RWA协议的TVL是多少？"

    print("Running Day17 pipeline...")

    result = run_llm_quality_pipeline(
        question=question,
        limit=3,
    )

    print("Building Day18 report...")

    report = build_research_report(
        question=question,
        pipeline_result=result,
    )

    markdown = render_markdown(report)

    print("\n=== GENERATED REPORT ===\n")
    print(markdown)

    assert report.metadata.snapshot_id
    assert report.quality.total_claims >= 0
    assert "## Market Overview" in markdown
    assert "## Research Quality" in markdown

    print("\nReport builder integration test passed!")


if __name__ == "__main__":
    main()
