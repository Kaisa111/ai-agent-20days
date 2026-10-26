
import re

from day17.schemas import ResearchEvidence
from day17.source_registry import (
    create_source_id,
)


def extract_tvl_claims(
    report_text: str,
    snapshot_id: str,
    protocols: list[dict],
) -> list[ResearchEvidence]:
    """
    Extract TVL claims from a research report.

    Only supports the standardized English format:
    <Protocol> has a reported TVL of $<amount> USD.

    Unsupported wording is not extracted.
    """

    evidence_list = []

    for protocol in protocols:
        name = protocol.get("name")

        if not isinstance(name, str) or not name:
            continue

        pattern = (
            rf"(?<!\w){re.escape(name)}"
            rf" has a reported TVL of "
            rf"\$[\d,]+(?:\.\d+)? USD\."
        )

        matches = re.finditer(
            pattern,
            report_text,
            flags=re.IGNORECASE,
        )

        for match in matches:
            source_id = (
                f"{snapshot_id}:"
                f"{create_source_id(protocol)}"
            )

            evidence_list.append(
                ResearchEvidence(
                    claim=match.group(0),
                    source_type="api",
                    source_id=source_id,
                    evidence_text=(
                        f"Protocol: {name}; "
                        f"TVL_USD: {protocol['tvl']:,.2f}; "
                        "Source: DefiLlama"
                    ),
                )
            )

    return evidence_list
