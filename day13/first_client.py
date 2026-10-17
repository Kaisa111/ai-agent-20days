import json
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # 1. Configure the MCP server process
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "day13.first_server"],
    )

    # 2. Start server and establish stdio connection
    async with stdio_client(server_params) as (read, write):

        # 3. Create MCP session
        async with ClientSession(read, write) as session:

            # 4. Initialize the MCP connection
            await session.initialize()

            print("MCP connection established!")

            # 5. Discover available tools
            tools = await session.list_tools()

            print("\n=== Available Tools ===")

            for tool in tools.tools:
                print(f"Name: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Input Schema: {tool.input_schema}")

            # 6. Call an MCP tool
            print("\n=== Calling MCP Tool ===")

            result = await session.call_tool(
                "calculate_btc_value",
                arguments={
                    "btc_amount": 0.5,
                    "btc_price_usd": 100000,
                },
            )

            print("Tool result:")
            print(result)

            assert not result.is_error, "MCP tool returned an error"

            # Extract the JSON returned by the MCP tool
            data = json.loads(result.content[0].text)

            # Verify the calculation
            assert data["total_value_usd"] == 50000.0

            print(f"\nVerified BTC position value: ${data['total_value_usd']:,.2f}")
            print("MCP Client Test PASSED")


if __name__ == "__main__":
    asyncio.run(main())
