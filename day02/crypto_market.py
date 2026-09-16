import requests


def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum,solana",
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

        return response.json()

    except requests.RequestException as e:
        print(f"CoinGecko 请求失败: {e}")
        return None


def calculate_market_average(data):
    changes = []

    for coin_id in data:
        change = data[coin_id].get("usd_24h_change")

        if change is not None:
            changes.append(change)

    if len(changes) == 0:
        return None

    return sum(changes) / len(changes)


def get_market_status(avg_change):
    if avg_change is None:
        return "Unknown"

    if avg_change > 2:
        return "Bullish"

    elif avg_change < -2:
        return "Bearish"

    else:
        return "Neutral"


def display_market(data, avg_change, market_status):
    symbols = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "solana": "SOL"
    }

    print("\n===== Crypto Market CLI =====\n")

    for coin_id, symbol in symbols.items():
        coin_data = data.get(coin_id)

        if coin_data is None:
            print(f"{symbol}: Data unavailable")
            print()
            continue

        price = coin_data.get("usd")
        change = coin_data.get("usd_24h_change")

        print(symbol)

        if price is not None:
            print(f"Price: ${price:,.2f}")
        else:
            print("Price: N/A")

        if change is not None:
            print(f"24h Change: {change:+.2f}%")
        else:
            print("24h Change: N/A")

        print()

    if avg_change is not None:
        print(f"Average Change: {avg_change:+.2f}%")
    else:
        print("Average Change: N/A")

    print(f"Market Status: {market_status}")


def main():
    data = fetch_crypto_data()

    if data is None:
        print("无法获取市场数据，程序结束。")
        return

    avg_change = calculate_market_average(data)

    market_status = get_market_status(avg_change)

    display_market(
        data,
        avg_change,
        market_status
    )


if __name__ == "__main__":
    main()