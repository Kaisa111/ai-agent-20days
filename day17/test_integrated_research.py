
from day17.integrated_research import (
    run_integrated_research,
)


def main():
    result = run_integrated_research(
        question="目前主要RWA协议的TVL是多少？",
        limit=3,
    )

    print("\nQUESTION")
    print(result["question"])

    print("\nSNAPSHOT")
    print(result["snapshot"]["snapshot_id"])

    print("\nVALIDATED CLAIMS")

    for evidence in result["evidence"]:
        print(
            evidence["claim"],
            "|",
            evidence["verification_status"],
        )

    print("\nQUALITY REPORT")

    report = result["quality_report"]

    for key, value in report.items():
        print(f"{key}: {value}")

    print("\nQUALITY SCOPE")
    print(result["quality_scope"])

    assert report["total_claims"] == 3
    assert report["verified_claims"] == 3
    assert report["contradicted_claims"] == 0
    assert report["evidence_coverage"] == 1.0

    print("\nIntegrated research test passed!")


if __name__ == "__main__":
    main()
