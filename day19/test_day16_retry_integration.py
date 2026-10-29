
from unittest.mock import patch

from day16.rwa_data import get_rwa_protocols


def main():
    # Mock DefiLlama API response
    fake_protocols = [
        {
            "name": "Protocol A",
            "category": "RWA",
            "tvl": 100_000_000,
            "symbol": "A",
            "chains": ["Ethereum"],
        },
        {
            "name": "Protocol B",
            "category": "RWA",
            "tvl": 300_000_000,
            "symbol": "B",
            "chains": ["Ethereum"],
        },
        {
            "name": "Protocol C",
            "category": "DEX",
            "tvl": 900_000_000,
        },
        {
            "name": "Protocol D",
            "category": "RWA",
            "tvl": None,
        },
    ]

    with patch(
        "day16.rwa_data.get_json_with_retry",
        return_value=fake_protocols,
    ) as mock_fetch:

        result = get_rwa_protocols(limit=2)

        mock_fetch.assert_called_once()

    print("=== FILTERED RWA PROTOCOLS ===")

    for protocol in result:
        print(
            f"{protocol['name']}: "
            f"${protocol['tvl']:,.0f}"
        )

    # Only valid RWA protocols remain.
    assert len(result) == 2

    # Results must be sorted by TVL.
    assert result[0]["name"] == "Protocol B"
    assert result[1]["name"] == "Protocol A"

    # Non-RWA and invalid TVL excluded.
    assert all(
        protocol["category"] == "RWA"
        for protocol in result
    )

    print("\nDay16 retry integration tests passed!")


if __name__ == "__main__":
    main()
