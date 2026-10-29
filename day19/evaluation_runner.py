
import time
from datetime import datetime, timezone
from uuid import uuid4

from common.token_tracker import (
    start_tracking,
    get_usage,
    stop_tracking,
)
from day17.llm_quality_pipeline import (
    run_llm_quality_pipeline,
)
from day19.evaluation_schemas import AgentRunRecord

from common.cost_calculator import calculate_api_cost

def evaluate_agent(
    question: str,
    limit: int = 3,
) -> AgentRunRecord:
    """
    Run the RWA research pipeline and
    collect execution and token metrics.
    """

    if limit < 1:
        raise ValueError("limit must be at least 1")

    run_id = f"run_{uuid4().hex[:12]}"
    started_at_utc = datetime.now(
        timezone.utc
    ).isoformat()

    start = time.perf_counter()

    # Start a new token tracking scope.
    tracking_token = start_tracking()

    # Initialize metrics for this run.
    success = False
    evidence_coverage = 0.0
    claim_completeness = 0.0
    error_message = None
    usage = None

    try:
        result = run_llm_quality_pipeline(
            question=question,
            limit=limit,
        )

        quality = result["quality_report"]
        coverage = result["coverage_report"]

        evidence_coverage = quality[
            "evidence_coverage"
        ]
        claim_completeness = coverage[
            "claim_completeness"
        ]

        success = True

    except Exception as exc:
        error_message = (
            f"{type(exc).__name__}: {exc}"
        )

    finally:
        # Collect usage even when the pipeline fails.
        usage = get_usage()

        # Always restore the previous tracking scope.
        stop_tracking(tracking_token)

        latency = time.perf_counter() - start

    # Zero API calls does not necessarily mean
    # zero tokens were consumed.
    has_usage = (
        usage is not None
        and usage.api_calls > 0
    )

    estimated_cost = None

    if has_usage:
        estimated_cost = calculate_api_cost(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cached_input_tokens=usage.cached_input_tokens,
        )

    return AgentRunRecord(
        run_id=run_id,
        question=question,
        started_at_utc=started_at_utc,
        success=success,
        latency_seconds=latency,
        evidence_coverage=evidence_coverage,
        claim_completeness=claim_completeness,
        input_tokens=(
            usage.input_tokens
            if has_usage else None
        ),
        output_tokens=(
            usage.output_tokens
            if has_usage else None
        ),
        estimated_cost_usd=estimated_cost,
        error_message=error_message,
    )
