
import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "day13.crypto_server"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("[MCP] Connected to Crypto Server")

            # 1. Discover tools
            tools = await session.list_tools()

            print("\n=== Available Tools ===")

            tool_names = []

            for tool in tools.tools:
                tool_names.append(tool.name)
                print(f"Name: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Input Schema: {tool.input_schema}")

            assert "crypto_price" in tool_names, (
                "crypto_price tool not found"
            )

            # 2. Call the real market data tool
            print("\n=== Querying Bitcoin Price ===")

            result = await session.call_tool(
                "crypto_price",
                arguments={
                    "symbol": "BTC",
                },
            )

            if result.is_error:
                raise RuntimeError(
                    f"MCP tool failed: {result.content}"
                )


            # 3. Parse and validate response

            parsed_data = None

            for item in result.content:

                if item.type == "text":

                    try:
                        parsed_data = json.loads(item.text)

                        print(
                            json.dumps(
                                parsed_data,
                                indent=2,
                                ensure_ascii=False,
                            )
                        )

                    except json.JSONDecodeError:
                        print(item.text)

            # Validate MCP response
            assert not result.is_error, "MCP protocol/tool error"

            # Validate business response
            assert isinstance(parsed_data, dict), (
                "Invalid response format"
            )

            market_data = parsed_data.get("data")

            assert isinstance(market_data, dict), (
                "Invalid market data format"
            )

            assert "error" not in market_data, (
                f"Business error: {market_data.get('error')}"
            )

            assert market_data.get("symbol") == "BTC", (
                "Unexpected cryptocurrency symbol"
            )

            assert isinstance(
                market_data.get("price_usd"), (int, float)
            ), "Missing or invalid BTC price"

            assert market_data["price_usd"] > 0, (
                "BTC price must be positive"
            )

            assert isinstance(
                market_data.get("change_24h"), (int, float)
            ), "Missing or invalid 24h change"            

            print("\nCrypto MCP Tool Test PASSED")



if __name__ == "__main__":
    asyncio.run(main())
