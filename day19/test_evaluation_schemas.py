
from pydantic import ValidationError

from day19.evaluation_schemas import (
    AgentRunRecord,
    EvaluationSummary,
)


def main():
    run = AgentRunRecord(
        run_id="run_001",
        question="目前主要RWA协议的TVL是多少？",
        success=True,
        latency_seconds=8.5,
        evidence_coverage=1.0,
        claim_completeness=1.0,
    )

    print("=== AGENT RUN ===")
    print(run.model_dump_json(indent=2))

    assert run.success is True
    assert run.input_tokens is None
    assert run.estimated_cost_usd is None

    summary = EvaluationSummary(
        total_runs=3,
        successful_runs=2,
        failed_runs=1,
        success_rate=2 / 3,
        average_latency_seconds=9.2,
        p95_latency_seconds=12.5,
        average_evidence_coverage=0.8,
        average_claim_completeness=0.9,
    )

    print("\n=== EVALUATION SUMMARY ===")
    print(summary.model_dump_json(indent=2))

    assert summary.total_runs == 3

    # Invalid coverage must be rejected.
    try:
        AgentRunRecord(
            run_id="invalid",
            question="Test",
            latency_seconds=1.0,
            evidence_coverage=1.5,
        )
    except ValidationError:
        print("\nInvalid coverage correctly rejected.")
    else:
        raise AssertionError(
            "Invalid coverage was not rejected."
        )

    print("\nEvaluation schema tests passed!")


if __name__ == "__main__":
    main()
