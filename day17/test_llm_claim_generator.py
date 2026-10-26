
from day16.rwa_market_agent import (
    run_rwa_market_research,
)

from day17.llm_claim_generator import (
    generate_tvl_claims,
)


def main():
    research = run_rwa_market_research(
        question="主要RWA协议的TVL是多少？",
        limit=3,
        include_live_data=True,
        include_rag=False,
    )

    market_data = research["market_data"]

    report = generate_tvl_claims(
        market_data
    )

    print("\nLLM GENERATED CLAIMS")

    for claim in report.claims:
        print(
            f"{claim.protocol_name}: "
            f"${claim.reported_tvl_usd:,.2f}"
        )

    assert len(report.claims) == 3

    print("\nLLM claim generation test passed!")


if __name__ == "__main__":
    main()
