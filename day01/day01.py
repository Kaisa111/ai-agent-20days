dict = {
'name': 'BTC',
'price': 100000,
'change': 2.35
}
print(f'比特币当前价格：{dict["price"]}美元\n24小时涨跌幅：{dict["change"]}%')

prices = [100000, 101000, 99000, 102000, 103000]
print(f"最高价：{max(prices)}美元\n最低价：{min(prices)}美元")

asset = {
    "name": "Bitcoin",
    "symbol": "BTC",
    "price": 100000,
    "change_24h": 2.35
}
print(f"资产名称: {asset['name']}")
print(f"交易代码: {asset['symbol']}")
print(f"当前价格: {asset['price']}美元")
print(f"24小时涨跌: {asset['change_24h']}%")

def calculate_change(current_price, previous_price):
    return (current_price - previous_price) / previous_price * 100

if change > 5:
    print("强势上涨")
elif change < -5:
    print("强势下跌")
else:
    print("震荡")