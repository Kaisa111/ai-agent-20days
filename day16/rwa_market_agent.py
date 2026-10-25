
import json
from datetime import datetime, timezone

from day09.rag_graph import rwa_node
from day16.rwa_tools import get_top_rwa_protocols


def run_rwa_market_research(
    question: str,
    limit: int = 5,
    include_live_data: bool = True,
    include_rag: bool = True,
) -> dict:
    """
    Combine local RAG research with live RWA data.
    """

    print("\n[Day16] Starting RWA market research...")

    # 1. Retrieve knowledge from local RAG

    rag_answer = None

    if include_rag:
        print("[Day16] Running RAG research...")

        rag_result = rwa_node({
            "question": question,
            "category": "rwa",
            "answer": "",
        })

        rag_answer = rag_result["answer"]
    else:
        print("[Day16] RAG research skipped.")


    # 2. Fetch live market data

    market_data = None

    if include_live_data:
        print("[Day16] Fetching live market data...")

        market_data = json.loads(
            get_top_rwa_protocols.invoke({
                "limit": limit,
            })
        )
    else:
        print("[Day16] Live market data skipped.")


    # 3. Record the retrieval timestamp
    retrieved_at = datetime.now(
        timezone.utc
    ).isoformat()


    return {
        "question": question,
        "rag_answer": rag_answer,
        "market_data": market_data,
        "retrieved_at_utc": retrieved_at,
        "live_data_requested": include_live_data,
    }



if __name__ == "__main__":
    result = run_rwa_market_research(
        question=(
            "What are the main risks of investing "
            "in RWA protocols?"
        ),
        limit=3,
    )

    print("\n=== RAG Research ===")
    print(result["rag_answer"])

    print("\n=== Live Market Data ===")

    for protocol in result["market_data"]["protocols"]:
        print(
            f"{protocol['name']}: "
            f"${protocol['tvl']:,.2f}"
        )

    print("\nRetrieved at (UTC):")
    print(result["retrieved_at_utc"])
