
from day12.fault_tolerant_agents import run_parallel_safe

from day15.agents import (
    run_crypto_agent,
    run_rwa_agent,
)


def run_research_agents(crypto_question: str, rwa_question: str):
    """Run real Crypto and RWA agents concurrently."""

    print("\n[Day15] Starting parallel research...")

    results = run_parallel_safe(
        crypto_question=crypto_question,
        rwa_question=rwa_question,
        crypto_func=run_crypto_agent,
        rwa_func=run_rwa_agent,
    )

    print("\n=== Agent Execution Status ===")

    for name in ["crypto", "rwa"]:
        result = results[name]

        print(f"{name}: {result['status']}")

        if result["status"] == "failed":
            print(f"Error: {result['error']}")

    print(f"\nElapsed: {results['elapsed']:.2f}s")

    return results


if __name__ == "__main__":

    results = run_research_agents(
        crypto_question=(
            "Analyze Bitcoin investment risks, "
            "including market volatility and custody."
        ),
        rwa_question=(
            "Analyze the liquidity, custody, and legal "
            "risks of tokenized Treasury bonds."
        ),
    )

    for name in ["crypto", "rwa"]:
        print(f"\n=== {name.upper()} Research ===")

        if results[name]["status"] == "success":
            print(results[name]["answer"])
        else:
            print("Research unavailable.")
