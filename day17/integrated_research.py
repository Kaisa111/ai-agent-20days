
import math

from day16.rwa_market_agent import (
    run_rwa_market_research,
)

from day17.schemas import ResearchEvidence

from day17.market_snapshot import (
    create_market_snapshot,
    build_snapshot_registry,
)

from day17.source_registry import (
    create_source_id,
    validate_registered_numeric_evidence,
)

from day17.quality_scorer import (
    calculate_research_quality,
)


def run_integrated_research(
    question: str,
    limit: int = 3,
) -> dict:
    """
    Run Day16 research and Day17 quality checks.

    This version validates standardized TVL
    claims generated from the API snapshot.
    It does not yet extract claims from the
    Agent's natural-language report.
    """

    # Step 1: Run the existing Day16 Agent
    research = run_rwa_market_research(
        question=question,
        limit=limit,
        include_live_data=True,
        include_rag=False,
    )

    market_data = research.get("market_data")

    if not isinstance(market_data, dict):
        raise ValueError(
            "Day16 returned invalid market_data"
        )

    if (
        market_data.get("source") != "DefiLlama"
        or market_data.get("metric") != "TVL_USD"
    ):
        raise ValueError(
            "Unsupported market data source or metric"
        )

    protocols = market_data.get("protocols", [])

    if not isinstance(protocols, list) or not protocols:
        raise ValueError(
            "No valid protocol list returned"
        )

    # Step 2: Create snapshot and registry
    snapshot = create_market_snapshot(
        protocols
    )

    registry = build_snapshot_registry(
        snapshot
    )

    evidence_list = []

    # Step 3: Generate and validate claims
    for protocol in snapshot.protocols:
        name = protocol.get("name")
        tvl = protocol.get("tvl")

        if (
            not isinstance(name, str)
            or not name
            or isinstance(tvl, bool)
            or not isinstance(tvl, (int, float))
            or not math.isfinite(tvl)
            or tvl < 0
        ):
            continue

        source_id = (
            f"{snapshot.snapshot_id}:"
            f"{create_source_id(protocol)}"
        )

        evidence = ResearchEvidence(
            claim=(
                f"{name} has a reported TVL "
                f"of ${tvl:,.2f} USD."
            ),
            source_type="api",
            source_id=source_id,
            evidence_text=(
                f"Protocol: {name}; "
                f"TVL_USD: {tvl:,.2f}; "
                "Source: DefiLlama"
            ),
        )

        validated = (
            validate_registered_numeric_evidence(
                evidence,
                registry,
            )
        )

        evidence_list.append(validated)

    # Step 4: Calculate quality metrics
    quality_report = calculate_research_quality(
        evidence_list
    )

    return {
        "question": question,
        "research": research,
        "snapshot": snapshot.model_dump(),
        "evidence": [
            e.model_dump()
            for e in evidence_list
        ],
        "quality_report": quality_report.model_dump(),
        "quality_scope": (
            "API-derived TVL claim consistency only. "
            "Agent-generated narrative claims and "
            "RAG evidence are not yet evaluated."
        ),
    }
