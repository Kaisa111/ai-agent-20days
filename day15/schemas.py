
from typing import Literal
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=5,
        description="用户提出的研究问题"
    )

    depth: Literal["quick", "standard", "deep"] = "standard"


class ResearchReport(BaseModel):
    question: str
    summary: str
    evidence: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
