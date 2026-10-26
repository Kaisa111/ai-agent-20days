
import argparse

from day17.llm_quality_pipeline import (
    run_llm_quality_pipeline,
)
from day18.report_builder import build_research_report
from day18.report_publisher import publish_report

from day18.snapshot_store import save_snapshot

def main():
    parser = argparse.ArgumentParser(
        description="Generate a validated RWA research report."
    )

    parser.add_argument(
        "--question",
        type=str,
        default="目前主要RWA协议的TVL是多少？",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=3,
    )

    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be at least 1")

    print("\n[1/4] Running RWA research pipeline...")

    pipeline_result = run_llm_quality_pipeline(
        question=args.question,
        limit=args.limit,
    )

    print("\n[2/5] Saving market snapshot...")

    snapshot_path = save_snapshot(
        pipeline_result["snapshot"]
    )

    print("Snapshot saved:", snapshot_path)

    print("\n[3/5] Building structured report...")

    report = build_research_report(
        question=args.question,
        pipeline_result=pipeline_result,
    )

    print("\n[4/5] Checking quality and saving report...")

    result = publish_report(report)

    print("\n[5/5] Completed.")

    print("\n=== REPORT RESULT ===")
    print("Status:", report.overall_status)
    print("Published:", result.published)
    print("File:", result.file_path)
    print("Snapshot:", snapshot_path)

    print(
        "Evidence coverage:",
        f"{report.quality.evidence_coverage:.2%}",
    )

    print(
        "Claim completeness:",
        f"{report.quality.claim_completeness:.2%}",
    )

    if result.reasons:
        print("\nReview reasons:")
        for reason in result.reasons:
            print("-", reason)


if __name__ == "__main__":
    main()
