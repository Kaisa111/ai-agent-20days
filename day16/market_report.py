
from datetime import datetime


def generate_market_report(research: dict) -> str:
    """Generate a readable report from RAG and API data."""

    question = research["question"]
    rag_answer = research["rag_answer"]
    market_data = research["market_data"]
    retrieved_at = research["retrieved_at_utc"]

    lines = [
        "# RWA Research Report",
        "",
        "## Research Question",
        question,
        "",
    ]

    if market_data is not None:
        lines.extend([
            "## Live RWA Market Data",
            "",
            "| Rank | Protocol | TVL (USD) | Chains |",
            "|---|---|---:|---|",
        ])

        for rank, protocol in enumerate(
            market_data["protocols"],
            start=1,
        ):
            chains = ", ".join(protocol["chains"])

            lines.append(
                f"| {rank} | {protocol['name']} | "
                f"${protocol['tvl']:,.2f} | {chains} |"
            )

        lines.extend([
            "",
            f"**Source:** {market_data['source']}",
            f"**API:** {market_data['endpoint']}",
            f"**Retrieved at (UTC):** {retrieved_at}",
            "",
            f"**Data limitation:** {market_data['limitations']}",
            "",
        ])


    if rag_answer:
        lines.extend([
            "## Knowledge Base Findings",
            "",
            rag_answer,
            "",
        ])

    lines.extend([
        "## Research Limitations",
        "",
        "Knowledge-base citations refer to local "
        "documents. Market figures come from the "
        "specified API and may change over time.",
    ])

    return "\n".join(lines)
