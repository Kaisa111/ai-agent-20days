
import math

from day16.rwa_data import get_rwa_protocols

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


def run_live_quality_pipeline(limit: int = 3):
    """
    Fetch live RWA data and evaluate TVL claims.

    Results measure consistency with the API
    snapshot, not independent market accuracy.
    """

    # Step 1: Fetch live market data
    protocols = get_rwa_protocols(limit=limit)

    if not protocols:
        raise RuntimeError(
            "No RWA protocols returned"
        )

    # Step 2: Freeze the market data
    snapshot = create_market_snapshot(
        protocols
    )

    # Step 3: Build source registry
    registry = build_snapshot_registry(
        snapshot
    )

    evidence_list = []

    # Step 4: Generate claims from snapshot
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

        # Step 5: Validate against snapshot
        validated = (
            validate_registered_numeric_evidence(
                evidence,
                registry,
            )
        )

        evidence_list.append(validated)

    # Step 6: Calculate quality metrics
    quality_report = calculate_research_quality(
        evidence_list
    )

    return snapshot, evidence_list, quality_report
