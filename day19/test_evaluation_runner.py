
from unittest.mock import patch

from day19.evaluation_runner import evaluate_agent


def fake_pipeline(question, limit):
    return {
        "quality_report": {
            "evidence_coverage": 1.0,
        },
        "coverage_report": {
            "claim_completeness": 1.0,
        },
    }


def failing_pipeline(question, limit):
    raise RuntimeError("Simulated API failure")


def main():
    with patch(
        "day19.evaluation_runner.run_llm_quality_pipeline",
        side_effect=fake_pipeline,
    ):
        good = evaluate_agent(
            question="RWA TVL test",
            limit=3,
        )

    print("Successful run:")
    print(good.model_dump_json(indent=2))

    assert good.success
    assert good.evidence_coverage == 1.0
    assert good.claim_completeness == 1.0
    assert good.latency_seconds >= 0

    with patch(
        "day19.evaluation_runner.run_llm_quality_pipeline",
        side_effect=failing_pipeline,
    ):
        bad = evaluate_agent(
            question="RWA failure test",
            limit=3,
        )

    print("\nFailed run:")
    print(bad.model_dump_json(indent=2))

    assert not bad.success
    assert "Simulated API failure" in bad.error_message
    assert bad.evidence_coverage == 0.0

    print("\nEvaluation runner tests passed!")


if __name__ == "__main__":
    main()
