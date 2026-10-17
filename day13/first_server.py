
from mcp.server import MCPServer

# Create an MCP server
mcp = MCPServer("Crypto Research Tools")


@mcp.tool()
def calculate_btc_value(
    btc_amount: float,
    btc_price_usd: float,
) -> dict:
    """Calculate the USD value of a Bitcoin position."""

    if btc_amount < 0 or btc_price_usd < 0:
        raise ValueError("Amount and price must be non-negative")

    total_value = btc_amount * btc_price_usd

    return {
        "btc_amount": btc_amount,
        "btc_price_usd": btc_price_usd,
        "total_value_usd": round(total_value, 2),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
