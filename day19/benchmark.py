
import math
from statistics import mean

from day19.evaluation_schemas import (
    AgentRunRecord,
    EvaluationSummary,
)


def calculate_p95(values: list[float]) -> float:
    """
    Calculate P95 using nearest-rank method.
    """
    if not values:
        return 0.0

    sorted_values = sorted(values)
    index = math.ceil(0.95 * len(sorted_values)) - 1

    return sorted_values[index]


def summarize_runs(
    runs: list[AgentRunRecord],
) -> EvaluationSummary:
    """
    Aggregate Agent evaluation metrics.
    """

    total = len(runs)
    successful = sum(run.success for run in runs)
    failed = total - successful

    latencies = [
        run.latency_seconds for run in runs
    ]

    # Research quality is evaluated only for
    # runs that completed successfully.
    completed = [
        run for run in runs if run.success
    ]

    costs = [
        run.estimated_cost_usd
        for run in runs
    ]

    # Only report a total cost if every run
    # has known cost data.

    # Include known costs from both successful
    # and failed runs.
    known_costs = [
        cost for cost in costs
        if cost is not None
    ]

    # None means no cost data is available.
    # Partial totals are lower bounds, not
    # necessarily the complete API bill.
    total_cost = (
        sum(known_costs)
        if known_costs else None
    )


    return EvaluationSummary(
        total_runs=total,
        successful_runs=successful,
        failed_runs=failed,
        success_rate=(
            successful / total if total else 0.0
        ),
        average_latency_seconds=(
            mean(latencies) if latencies else 0.0
        ),
        p95_latency_seconds=calculate_p95(latencies),
        average_evidence_coverage=(
            mean(
                run.evidence_coverage
                for run in completed
            )
            if completed else 0.0
        ),
        average_claim_completeness=(
            mean(
                run.claim_completeness
                for run in completed
            )
            if completed else 0.0
        ),
        total_estimated_cost_usd=total_cost,
    )
