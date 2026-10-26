
from day17.schemas import ResearchEvidence
from day17.quality_scorer import (
    calculate_research_quality,
)


def make_evidence(status: str, index: int):
    return ResearchEvidence(
        claim=f"Research claim {index}",
        source_type="knowledge_base",
        source_id=f"Chunk {index}",
        evidence_text=f"Evidence for claim {index}",
        verification_status=status,
    )


evidence_list = []

# 7 supported claims
for i in range(7):
    evidence_list.append(
        make_evidence("verified", i)
    )

# 2 unsupported claims
for i in range(7, 9):
    evidence_list.append(
        make_evidence("unverified", i)
    )

# 1 contradicted claim
evidence_list.append(
    make_evidence("contradicted", 9)
)

report = calculate_research_quality(
    evidence_list
)

print(report.model_dump_json(indent=2))

assert report.total_claims == 10
assert report.verified_claims == 7
assert report.unverified_claims == 2
assert report.contradicted_claims == 1
assert report.evidence_coverage == 0.7

print("\nAll quality scoring tests passed!")
