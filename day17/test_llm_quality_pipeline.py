
from day17.llm_quality_pipeline import (
    run_llm_quality_pipeline,
)


def main():
    result = run_llm_quality_pipeline(
        question="目前主要RWA协议的TVL是多少？",
        limit=3,
    )

    print("\nSNAPSHOT")
    print(result["snapshot"]["snapshot_id"])

    print("\nLLM CLAIM VERIFICATION")

    for evidence in result["evidence"]:
        print(
            evidence["claim"],
            "|",
            evidence["verification_status"],
        )

    print("\nQUALITY REPORT")

    report = result["quality_report"]
    print(report)

    assert report["total_claims"] == 3

    assert (
        report["verified_claims"]
        + report["unverified_claims"]
        + report["contradicted_claims"]
        == 3
    )

    print("\nLLM quality pipeline test passed!")


if __name__ == "__main__":
    main()
