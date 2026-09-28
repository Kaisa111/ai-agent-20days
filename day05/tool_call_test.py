from openai import OpenAI
from dotenv import load_dotenv
from tools import get_crypto_price, calculate_position

import os
import json


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================
# Tool Definitions
# 告诉 LLM：有哪些工具可以使用
# =========================

tools = [
    {
        "type": "function",
        "name": "get_crypto_price",
        "description": "Get the current USD price and 24-hour price change of a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Cryptocurrency symbol such as BTC, ETH, or SOL."
                }
            },
            "required": ["symbol"]
        }
    }
    ,
    {
    "type": "function",
    "name": "calculate_position",
    "description": "Calculate how much of an asset can be purchased for a given USD investment amount and asset price.",
    "parameters": {
        "type": "object",
        "properties": {
            "investment_usd": {
                "type": "number",
                "description": "Amount of USD to invest."
            },
            "asset_price_usd": {
                "type": "number",
                "description": "Price of one unit of the asset in USD."
            }
        },
        "required": [
            "investment_usd",
            "asset_price_usd"
        ]
    }
    }
]


# =========================
# Tool Registry
# 告诉 Python：工具名称对应哪个函数
# =========================

TOOL_FUNCTIONS = {
    "get_crypto_price": get_crypto_price,
    "calculate_position": calculate_position
}


# =========================
# First LLM Call
# =========================

response = client.responses.create(
    model="gpt-5.6-luna",

    instructions="""
    You are a crypto research assistant.

    Use available tools when the user asks for current
    cryptocurrency market data.

    After receiving tool results,
    answer clearly and concisely.
    """,

    tools=tools,

    input="""
I want to invest $10,000 in Bitcoin.
Use the current BTC price and tell me approximately
how much BTC I can buy.
"""
)


tool_outputs = []


# =========================
# Execute Tool Calls
# =========================

for item in response.output:

    if item.type != "function_call":
        continue

    print("\n===== Tool Call =====")
    print(f"Tool: {item.name}")
    print(f"Arguments: {item.arguments}")

    # JSON string → Python dict
    arguments = json.loads(item.arguments)

    # 从 Tool Registry 找到真正的 Python 函数
    tool_function = TOOL_FUNCTIONS.get(item.name)

    if tool_function is None:

        result = {
            "error": f"Unknown tool: {item.name}"
        }

    else:

        # 自动展开参数并执行函数
        result = tool_function(**arguments)

    print("\n===== Tool Result =====")
    print(result)

    tool_outputs.append(
        {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(result)
        }
    )


# =========================
# Second LLM Call
# =========================

if tool_outputs:

    final_response = client.responses.create(
        model="gpt-5.6-luna",

        previous_response_id=response.id,

        tools=tools,

        input=tool_outputs
    )

    print("\n===== Final Answer =====")
    print(final_response.output_text)

else:

    print("\n===== Final Answer =====")
    print(response.output_text)