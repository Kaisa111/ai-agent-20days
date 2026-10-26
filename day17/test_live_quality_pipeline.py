
from day17.live_quality_pipeline import (
    run_live_quality_pipeline,
)


def main():
    snapshot, evidence_list, report = (
        run_live_quality_pipeline(limit=3)
    )

    print("Snapshot:", snapshot.snapshot_id)
    print("Retrieved at:", snapshot.retrieved_at_utc)

    print("\nVALIDATED MARKET CLAIMS")

    for evidence in evidence_list:
        print(
            f"\nClaim: {evidence.claim}"
        )
        print(
            f"Source: {evidence.source_id}"
        )
        print(
            f"Status: {evidence.verification_status}"
        )

    print("\nRESEARCH QUALITY REPORT")
    print(report.model_dump_json(indent=2))

    assert len(evidence_list) == 3
    assert report.total_claims == 3
    assert report.verified_claims == 3
    assert report.contradicted_claims == 0
    assert report.evidence_coverage == 1.0

    print("\nLive quality pipeline test passed!")


if __name__ == "__main__":
    main()
