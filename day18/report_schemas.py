
from typing import Literal

from pydantic import BaseModel, Field


class ReportSection(BaseModel):
    """
    One section of a research report.
    """

    title: str
    content: str

    evidence_ids: list[str] = Field(
        default_factory=list
    )


class ReportMetadata(BaseModel):
    """
    Report metadata and data provenance.
    """

    title: str
    question: str
    generated_at_utc: str
    snapshot_id: str

    data_source: str = "DefiLlama"


class ReportQuality(BaseModel):
    """
    Quality metrics inherited from Day17.
    """

    total_claims: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0
    contradicted_claims: int = 0

    evidence_coverage: float = 0.0
    claim_completeness: float = 0.0


class ResearchReport(BaseModel):
    """
    Structured RWA research report.
    """

    metadata: ReportMetadata

    executive_summary: str

    sections: list[ReportSection] = Field(
        default_factory=list
    )

    quality: ReportQuality

    limitations: list[str] = Field(
        default_factory=list
    )

    overall_status: Literal[
        "verified",
        "partial",
        "requires_review",
    ] = "requires_review"
