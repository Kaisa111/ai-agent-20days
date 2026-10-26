
from day17.llm_quality_pipeline import (
    run_llm_quality_pipeline,
)


def main():
    result = run_llm_quality_pipeline(
        question="目前主要RWA协议的TVL是多少？",
        limit=3,
    )

    quality = result["quality_report"]
    coverage = result["coverage_report"]

    print("\n=== EVIDENCE QUALITY ===")
    print("Total claims:", quality["total_claims"])
    print("Verified:", quality["verified_claims"])
    print("Unverified:", quality["unverified_claims"])
    print("Contradicted:", quality["contradicted_claims"])
    print("Evidence coverage:", quality["evidence_coverage"])

    print("\n=== CLAIM COMPLETENESS ===")
    print("Expected protocols:", coverage["expected_protocols"])
    print("Generated claims:", coverage["generated_claims"])
    print("Covered protocols:", coverage["covered_protocols"])
    print("Missing:", coverage["missing_protocols"])
    print("Duplicates:", coverage["duplicate_protocols"])
    print("Unknown:", coverage["unknown_protocols"])
    print("Completeness:", coverage["claim_completeness"])

    # Validate report consistency
    assert quality["total_claims"] == len(
        result["evidence"]
    )

    assert (
        quality["verified_claims"]
        + quality["unverified_claims"]
        + quality["contradicted_claims"]
        == quality["total_claims"]
    )

    assert coverage["expected_protocols"] == 3

    assert (
        0.0 <= coverage["claim_completeness"] <= 1.0
    )

    assert (
        0.0 <= quality["evidence_coverage"] <= 1.0
    )

    print("\nFinal pipeline test passed!")


if __name__ == "__main__":
    main()
