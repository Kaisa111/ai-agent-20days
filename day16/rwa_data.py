
import requests


API_URL = "https://api.llama.fi/protocols"


def get_rwa_protocols(limit=10):
    """Fetch and rank RWA protocols by TVL."""

    response = requests.get(
        API_URL,
        timeout=30,
    )
    response.raise_for_status()

    protocols = response.json()

    rwa_protocols = []

    for protocol in protocols:
        category = protocol.get("category", "")

        if not isinstance(category, str):
            continue

        if "RWA" not in category.upper():
            continue

        tvl = protocol.get("tvl")

        if not isinstance(tvl, (int, float)):
            continue

        rwa_protocols.append({
            "name": protocol.get("name"),
            "category": category,
            "tvl": tvl,
            "symbol": protocol.get("symbol"),
            "chains": protocol.get("chains", []),
        })

    rwa_protocols.sort(
        key=lambda item: item["tvl"],
        reverse=True,
    )

    return rwa_protocols[:limit]


if __name__ == "__main__":
    print("[Day16] Fetching RWA protocols...\n")

    protocols = get_rwa_protocols(limit=10)

    if not protocols:
        print(
            "No RWA protocols matched the current "
            "category filter. Check API categories."
        )

    for index, protocol in enumerate(
        protocols,
        start=1,
    ):
        print(
            f"{index}. {protocol['name']}"
        )
        print(
            f"   Category: {protocol['category']}"
        )
        print(
            f"   TVL: ${protocol['tvl']:,.2f}"
        )
        print(
            f"   Chains: {', '.join(protocol['chains'])}"
        )
        print()
