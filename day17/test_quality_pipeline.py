
from day17.schemas import ResearchEvidence

from day17.quality_pipeline import (
    run_quality_pipeline,
)


source_text = (
    "Liquidity risk occurs when investors "
    "cannot easily buy or sell the tokenized asset."
)

trusted_sources = {
    "Chunk 4": source_text,
}


evidence_list = [
    ResearchEvidence(
        claim=(
            "Tokenized assets may be difficult "
            "to sell."
        ),
        source_type="knowledge_base",
        source_id="Chunk 4",
        evidence_text=source_text,
    ),
    ResearchEvidence(
        claim=(
            "Tokenized assets can always "
            "be sold easily."
        ),
        source_type="knowledge_base",
        source_id="Chunk 4",
        evidence_text=source_text,
    ),
    ResearchEvidence(
        claim=(
            "Tokenized assets guarantee "
            "a 15% annual return."
        ),
        source_type="knowledge_base",
        source_id="Chunk 4",
        evidence_text=source_text,
    ),
]


report = run_quality_pipeline(
    evidence_list,
    trusted_sources,
)

print("\nFINAL QUALITY REPORT")
print(report.model_dump_json(indent=2))

assert report.total_claims == 3
assert report.verified_claims == 1
assert report.contradicted_claims == 1
assert report.unverified_claims == 1

print("\nQuality pipeline test passed!")
