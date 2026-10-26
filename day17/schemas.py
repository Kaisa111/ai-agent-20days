
from typing import Literal
from pydantic import BaseModel, Field


class ResearchEvidence(BaseModel):
    """A piece of evidence supporting a research claim."""

    claim: str = Field(
        min_length=1,
        description="The claim being evaluated",
    )

    source_type: Literal[
        "api",
        "knowledge_base",
        "llm",
    ]

    source_id: str = Field(
        description="API endpoint or knowledge chunk ID"
    )

    evidence_text: str = Field(
        description="The actual supporting evidence"
    )

    verification_status: Literal[
        "verified",
        "unverified",
        "contradicted",
    ] = "unverified"


class RiskAssessment(BaseModel):
    """Structured assessment of an RWA risk."""

    risk_type: Literal[
        "credit",
        "liquidity",
        "legal",
        "custody",
        "smart_contract",
        "market",
        "other",
    ]

    description: str

    severity: Literal[
        "low",
        "medium",
        "high",
        "unknown",
    ] = "unknown"

    evidence: list[ResearchEvidence] = Field(
        default_factory=list
    )


class ResearchQualityReport(BaseModel):
    """Quality assessment of a research report."""

    total_claims: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0
    contradicted_claims: int = 0

    evidence_coverage: float = 0.0

    risks: list[RiskAssessment] = Field(
        default_factory=list
    )
