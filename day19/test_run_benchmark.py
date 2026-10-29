
from unittest.mock import patch

from day19.evaluation_schemas import AgentRunRecord
from day19.run_benchmark import run_benchmark


def fake_evaluate_agent(question, limit):
    return AgentRunRecord(
        run_id="mock_run",
        question=question,
        success=True,
        latency_seconds=5.0,
        evidence_coverage=1.0,
        claim_completeness=1.0,
    )


def main():
    with patch(
        "day19.run_benchmark.evaluate_agent",
        side_effect=fake_evaluate_agent,
    ) as mock_agent:

        records, summary = run_benchmark(
            question="RWA benchmark test",
            runs=3,
            limit=3,
        )

        assert mock_agent.call_count == 3

    assert len(records) == 3
    assert summary.total_runs == 3
    assert summary.successful_runs == 3
    assert summary.success_rate == 1.0
    assert summary.average_latency_seconds == 5.0
    assert summary.p95_latency_seconds == 5.0

    try:
        run_benchmark(
            question="Invalid test",
            runs=0,
        )
    except ValueError:
        print("\nInvalid run count correctly rejected.")
    else:
        raise AssertionError(
            "Invalid run count was not rejected."
        )

    print("\nBenchmark CLI tests passed!")


if __name__ == "__main__":
    main()
