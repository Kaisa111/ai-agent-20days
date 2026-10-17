
import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_crypto_mcp_async(symbol: str) -> dict:
    """
    Call the Crypto MCP Server and return
    validated market data as a Python dict.
    """

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "day13.crypto_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "crypto_price",
                arguments={"symbol": symbol},
            )

            if result.is_error:
                raise RuntimeError(
                    f"MCP tool execution failed: {result.content}"
                )

            text_items = [
                item.text
                for item in result.content
                if item.type == "text"
            ]

            if not text_items:
                raise ValueError("MCP returned no text data")

            response = json.loads(text_items[0])

            if not isinstance(response, dict):
                raise ValueError("Invalid MCP response format")

            market_data = response.get("data")

            if not isinstance(market_data, dict):
                raise ValueError("Missing market data")

            if "error" in market_data:
                raise RuntimeError(market_data["error"])

            if market_data.get("symbol") != symbol.upper():
                raise ValueError("Unexpected symbol")

            price = market_data.get("price_usd")

            if (
                not isinstance(price, (int, float))
                or isinstance(price, bool)
                or price <= 0
            ):
                raise ValueError("Invalid cryptocurrency price")

            return market_data


def call_crypto_mcp(symbol: str) -> dict:
    """
    Synchronous wrapper for ordinary Python code.
    Call only when no event loop is already running.
    """
    return asyncio.run(call_crypto_mcp_async(symbol))


if __name__ == "__main__":
    print("[MCP Adapter] Querying BTC...")

    data = call_crypto_mcp("BTC")

    print(json.dumps(data, indent=2))

    assert data["symbol"] == "BTC"
    assert data["price_usd"] > 0

    print("\nMCP Adapter Test PASSED")
