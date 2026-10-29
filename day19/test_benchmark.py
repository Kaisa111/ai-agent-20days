
from day19.benchmark import (
    calculate_p95,
    summarize_runs,
)
from day19.evaluation_schemas import AgentRunRecord



from datetime import datetime, timezone

from day19.evaluation_schemas import AgentRunRecord
from day19.benchmark import summarize_runs


def test_cost_aggregation():
    """Verify cost aggregation across multiple runs."""

    def make_record(run_id, cost):
        return AgentRunRecord(
            run_id=run_id,
            question="Cost aggregation test",
            started_at_utc=datetime.now(
                timezone.utc
            ).isoformat(),
            success=True,
            latency_seconds=1.0,
            evidence_coverage=1.0,
            claim_completeness=1.0,
            input_tokens=100,
            output_tokens=20,
            estimated_cost_usd=cost,
            error_message=None,
        )

    records = [
        make_record("run_1", 0.001),
        make_record("run_2", 0.002),
        make_record("run_3", 0.003),
    ]

    summary = summarize_runs(records)

    assert abs(
        summary.total_estimated_cost_usd - 0.006
    ) < 1e-12

    print("Cost aggregation test passed!")


def test_cost_aggregation_with_failures():
    """Include known costs from failed runs."""

    from datetime import datetime, timezone

    def make_record(run_id, success, cost):
        return AgentRunRecord(
            run_id=run_id,
            question="Failure cost test",
            started_at_utc=datetime.now(
                timezone.utc
            ).isoformat(),
            success=success,
            latency_seconds=1.0,
            evidence_coverage=1.0 if success else 0.0,
            claim_completeness=1.0 if success else 0.0,
            input_tokens=None,
            output_tokens=None,
            estimated_cost_usd=cost,
            error_message=(
                None if success else "Simulated failure"
            ),
        )

    records = [
        make_record("run_1", True, 0.001),
        make_record("run_2", False, 0.002),
        make_record("run_3", False, None),
    ]

    summary = summarize_runs(records)

    assert summary.total_runs == 3
    assert summary.successful_runs == 1
    assert summary.failed_runs == 2

    assert abs(
        summary.total_estimated_cost_usd - 0.003
    ) < 1e-12

    print("Failure cost aggregation test passed!")


def make_run(
    index: int,
    success: bool,
    latency: float,
    coverage: float = 0.0,
    completeness: float = 0.0,
):
    return AgentRunRecord(
        run_id=f"run_{index}",
        question="RWA benchmark",
        success=success,
        latency_seconds=latency,
        evidence_coverage=coverage,
        claim_completeness=completeness,
    )


def main():
    runs = [
        make_run(1, True, 5.0, 1.0, 1.0),
        make_run(2, True, 8.0, 0.8, 0.9),
        make_run(3, True, 10.0, 0.9, 0.8),
        make_run(4, False, 12.0),
        make_run(5, True, 15.0, 1.0, 1.0),
    ]

    summary = summarize_runs(runs)

    print("=== BENCHMARK SUMMARY ===")
    print(summary.model_dump_json(indent=2))

    assert summary.total_runs == 5
    assert summary.successful_runs == 4
    assert summary.failed_runs == 1
    assert summary.success_rate == 0.8

    assert summary.average_latency_seconds == 10.0
    assert summary.p95_latency_seconds == 15.0

    assert abs(
        summary.average_evidence_coverage - 0.925
    ) < 1e-9

    assert abs(
        summary.average_claim_completeness - 0.925
    ) < 1e-9

    assert summary.total_estimated_cost_usd is None

    # Edge cases
    assert calculate_p95([]) == 0.0
    assert calculate_p95([1, 2, 3, 4, 5]) == 5

    empty = summarize_runs([])
    assert empty.total_runs == 0
    assert empty.success_rate == 0.0

    print("\nBenchmark tests passed!")


if __name__ == "__main__":
    main()
    test_cost_aggregation()
    test_cost_aggregation_with_failures()
