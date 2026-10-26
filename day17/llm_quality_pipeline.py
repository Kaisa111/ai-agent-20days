
from day16.rwa_market_agent import (
    run_rwa_market_research,
)

from day17.llm_claim_generator import (
    generate_tvl_claims,
)
from day17.market_snapshot import (
    create_market_snapshot,
    build_snapshot_registry,
)
from day17.source_registry import (
    create_source_id,
    validate_registered_numeric_evidence,
)
from day17.schemas import ResearchEvidence
from day17.quality_scorer import (
    calculate_research_quality,
)

from day17.coverage_validator import (
    validate_claim_coverage,
)

def run_llm_quality_pipeline(
    question: str,
    limit: int = 3,
) -> dict:
    # 1. Fetch live data
    research = run_rwa_market_research(
        question=question,
        limit=limit,
        include_live_data=True,
        include_rag=False,
    )

    market_data = research["market_data"]

    if not isinstance(market_data, dict):
        raise ValueError("Invalid market data")

    if (
        market_data.get("source") != "DefiLlama"
        or market_data.get("metric") != "TVL_USD"
    ):
        raise ValueError("Unsupported data source")

    protocols = market_data["protocols"]

    # 2. Freeze the source data
    snapshot = create_market_snapshot(protocols)
    registry = build_snapshot_registry(snapshot)

    # 3. Generate independent LLM claims
    llm_report = generate_tvl_claims(market_data)

    # Check LLM claim completeness
    coverage_report = validate_claim_coverage(
        protocols=snapshot.protocols,
        claims=llm_report.claims,
    )

    # 4. Match claims to protocols
    protocol_map = {
        p["name"]: p
        for p in snapshot.protocols
    }

    validated = []

    for claim in llm_report.claims:
        protocol = protocol_map.get(
            claim.protocol_name
        )

        if protocol is None:
            evidence = ResearchEvidence(
                claim=(
                    f"{claim.protocol_name} has a reported "
                    f"TVL of ${claim.reported_tvl_usd:,.2f} USD."
                ),
                source_type="api",
                source_id="unknown",
                evidence_text="Protocol not found in snapshot",
                verification_status="unverified",
            )
        else:
            source_id = (
                f"{snapshot.snapshot_id}:"
                f"{create_source_id(protocol)}"
            )

            evidence = ResearchEvidence(
                claim=(
                    f"{claim.protocol_name} has a reported "
                    f"TVL of ${claim.reported_tvl_usd:,.2f} USD."
                ),
                source_type="api",
                source_id=source_id,
                evidence_text=(
                    f"Protocol: {protocol['name']}; "
                    f"TVL_USD: {protocol['tvl']:,.2f}; "
                    "Source: DefiLlama"
                ),
            )

            evidence = (
                validate_registered_numeric_evidence(
                    evidence,
                    registry,
                )
            )

        validated.append(evidence)

    quality = calculate_research_quality(validated)

    return {
        "snapshot": snapshot.model_dump(),
        "evidence": [
            e.model_dump()
            for e in validated
        ],
        "quality_report": quality.model_dump(),
        "coverage_report": coverage_report.model_dump(),
    }
