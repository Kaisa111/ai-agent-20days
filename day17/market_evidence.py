
import json

from day17.schemas import ResearchEvidence


def extract_market_evidence(
    market_data: dict | str,
) -> tuple[list[ResearchEvidence], dict[str, str]]:
    """
    Convert DefiLlama market data into
    traceable research evidence.

    Each protocol TVL becomes one claim.
    """

    if isinstance(market_data, str):
        market_data = json.loads(market_data)

    if not isinstance(market_data, dict):
        raise TypeError(
            "market_data must be a dict or JSON string"
        )

    source = market_data.get("source")
    metric = market_data.get("metric")

    if source != "DefiLlama":
        raise ValueError(
            "Unsupported market data source"
        )

    if metric != "TVL_USD":
        raise ValueError(
            "Unsupported market metric"
        )

    evidence_list = []
    trusted_sources = {}

    protocols = market_data.get(
        "protocols", []
    )

    for index, protocol in enumerate(
        protocols, start=1
    ):
        name = protocol.get("name")
        tvl = protocol.get("tvl")

        if not isinstance(name, str) or not name:
            continue

        if (
            isinstance(tvl, bool)
            or not isinstance(tvl, (int, float))
        ):
            continue

        source_id = f"DefiLlama:protocol:{index}"

        claim = (
            f"{name} has a reported TVL "
            f"of ${tvl:,.2f} USD."
        )

        source_text = (
            f"Protocol: {name}; "
            f"TVL_USD: {tvl:,.2f}; "
            f"Source: DefiLlama"
        )

        evidence = ResearchEvidence(
            claim=claim,
            source_type="api",
            source_id=source_id,
            evidence_text=source_text,
        )

        evidence_list.append(evidence)
        trusted_sources[source_id] = source_text

    return evidence_list, trusted_sources
