print("========================")
print("   Crypto Market")
print("========================")
print()
crypto_assets = [
    {
        "symbol": "BTC",
        "price": 113000,
        "previous_price": 108000
    },
    {
        "symbol": "ETH",
        "price": 4400,
        "previous_price": 4700
    },
    {
        "symbol": "SOL",
        "price": 225,
        "previous_price": 210
    }
]
def calculate_change(current_price, previous_price):
    if previous_price == 0:
        return None
    return (current_price - previous_price) / previous_price * 100
for asset in crypto_assets:
    symbol = asset.get("symbol")
    price = asset.get("price")
    previous_price = asset.get("previous_price")
    change = calculate_change(price, previous_price)
    print(symbol)
    print(f"Price: ${price:,}")
    if change is not None:
        def get_status(change):
            if change > 5:
                return "status:强势上涨"
            elif change < -5:
                return "status:强势下跌"
            else:
                return "status:震荡"
        print(f"24h Change: {change:+.2f}%")
        print(get_status(change))
    else:
        print("24h Change: N/A")
        print("Status: 数据异常")
    print()
print()

# Calculate average change
total_change = sum(asset.get("change_24h", 0) for asset in crypto_assets)
average_change = total_change / len(crypto_assets) if crypto_assets else 0

# Determine market status
if average_change > 2:
    print("Market Status: Bullish")
elif average_change < -2:
    print("Market Status: Bearish")
else:
    print("Market Status: Neutral")
print("========================")   