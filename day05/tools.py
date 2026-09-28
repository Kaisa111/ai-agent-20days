import requests


def get_crypto_price(symbol: str):

    symbol_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana"
    }

    symbol = symbol.upper()

    coin_id = symbol_map.get(symbol)

    if coin_id is None:
        return {
            "error": f"Unsupported symbol: {symbol}"
        }

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        coin_data = data.get(coin_id)

        if coin_data is None:
            return {
                "error": "Crypto data unavailable"
            }

        return {
            "symbol": symbol,
            "price_usd": coin_data.get("usd"),
            "change_24h": coin_data.get("usd_24h_change")
        }

    except requests.RequestException as e:
        return {
            "error": f"CoinGecko request failed: {e}"
        }

def calculate_position(
    investment_usd: float,
    asset_price_usd: float
):
    if asset_price_usd <= 0:
        return {
            "error": "Asset price must be greater than 0"
        }

    if investment_usd <= 0:
        return {
            "error": "Investment amount must be greater than 0"
        }

    quantity = investment_usd / asset_price_usd

    return {
        "investment_usd": investment_usd,
        "asset_price_usd": asset_price_usd,
        "quantity": quantity
    }