
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class AgentRunRecord(BaseModel):
    """
    Metrics for one Agent execution.
    """

    run_id: str
    question: str

    started_at_utc: str = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    success: bool = False
    latency_seconds: float = Field(ge=0)

    evidence_coverage: float = Field(
        default=0.0, ge=0, le=1
    )

    claim_completeness: float = Field(
        default=0.0, ge=0, le=1
    )

    input_tokens: int | None = Field(
        default=None, ge=0
    )

    output_tokens: int | None = Field(
        default=None, ge=0
    )

    estimated_cost_usd: float | None = Field(
        default=None, ge=0
    )

    error_message: str | None = None


class EvaluationSummary(BaseModel):
    """
    Aggregate metrics across Agent runs.
    """

    total_runs: int = Field(ge=0)
    successful_runs: int = Field(ge=0)
    failed_runs: int = Field(ge=0)

    success_rate: float = Field(ge=0, le=1)

    average_latency_seconds: float = Field(ge=0)
    p95_latency_seconds: float = Field(ge=0)

    average_evidence_coverage: float = Field(
        ge=0, le=1
    )

    average_claim_completeness: float = Field(
        ge=0, le=1
    )

    total_estimated_cost_usd: float | None = Field(
        default=None, ge=0
    )
