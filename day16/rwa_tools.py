
import json

from langchain_core.tools import tool

from day16.rwa_data import get_rwa_protocols


@tool
def get_top_rwa_protocols(limit: int = 10) -> str:
    """
    Get the top RWA protocols ranked by TVL
    from the DefiLlama API.

    Use this tool when researching RWA protocols,
    TVL rankings, or market activity.

    TVL is not the same as total tokenized
    real-world asset issuance.
    """

    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")

    protocols = get_rwa_protocols(limit=limit)

    return json.dumps(
        {
            "source": "DefiLlama",
            "endpoint": "https://api.llama.fi/protocols",
            "metric": "TVL_USD",
            "protocol_count": len(protocols),
            "protocols": protocols,
            "limitations": (
                "Results include only protocols whose "
                "category contains RWA. TVL does not "
                "represent total RWA issuance."
            ),
        },
        ensure_ascii=False,
    )
