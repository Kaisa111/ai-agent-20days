import asyncio

async def fetch_btc_price():
    await asyncio.sleep(2)
    print("BTC data received")

async def fetch_eth_price():
    await asyncio.sleep(3)
    print("ETH data received")

async def fetch_rwa_news():
    await asyncio.sleep(4)
    print("RWA news received")

async def main():
    await asyncio.gather(
        fetch_btc_price(), 
        fetch_eth_price(), 
        fetch_rwa_news()
    )

asyncio.run(main())