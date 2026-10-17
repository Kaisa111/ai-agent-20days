
from mcp.server import MCPServer
from day05.tools import get_crypto_price


mcp = MCPServer("Crypto Market MCP Server")


@mcp.tool()
def crypto_price(symbol: str) -> dict:
    """
    Get cryptocurrency market price information.

    Args:
        symbol: Cryptocurrency ticker, such as BTC, ETH, or SOL.
    """
    result = get_crypto_price(symbol)

    return {
        "symbol": symbol,
        "data": result,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
