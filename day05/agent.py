from openai import OpenAI
from dotenv import load_dotenv
from day05.tools import get_crypto_price, calculate_position

import os
import json


# =========================
# 1. Environment
# =========================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in .env")


client = OpenAI(api_key=api_key)


# =========================
# 2. Tool Definitions
# 给 LLM 看的工具说明书
# =========================

TOOLS = [
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
    },

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
                    "description": "USD price of one unit of the asset."
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
# 3. Tool Registry
# 给 Python 看的函数注册表
# =========================

TOOL_FUNCTIONS = {
    "get_crypto_price": get_crypto_price,
    "calculate_position": calculate_position
}


# =========================
# 4. Agent Loop
# =========================

def run_agent(user_message: str):

    # 第一次把用户问题交给 LLM
    response = client.responses.create(
        model="gpt-5.6-luna",

        instructions="""
        You are a crypto research assistant.

        Use get_crypto_price whenever current cryptocurrency market data is required.

        Use calculate_position whenever the user asks how much of an asset can be purchased for a given investment amount.

        Do not perform position calculations yourself.
        Always use calculate_position for position calculations.

        You may call tools across multiple steps.

        After you have enough information,
        answer the user's original question clearly and concisely.
        """,

        tools=TOOLS,

        input=user_message
    )


    # 最多允许 Agent 循环 10 轮
    for step in range(10):

        print(f"\n===== Agent Step {step + 1} =====")


        # 找出这一轮 LLM 要求执行的所有 Tool Calls
        tool_calls = []

        for item in response.output:

            if item.type == "function_call":
                tool_calls.append(item)


        # =========================
        # 没有 Tool Call
        # 说明 LLM 已经给出最终答案
        # =========================

        if len(tool_calls) == 0:

            print("No more tool calls.")

            return response.output_text


        # =========================
        # 执行这一轮所有 Tool Calls
        # =========================

        tool_outputs = []


        for tool_call in tool_calls:

            print(f"Tool: {tool_call.name}")
            print(f"Arguments: {tool_call.arguments}")


            # JSON string → Python dict
            try:

                arguments = json.loads(
                    tool_call.arguments
                )

            except json.JSONDecodeError:

                result = {
                    "error": "Invalid tool arguments"
                }

            else:

                # 找到真正的 Python Tool
                tool_function = TOOL_FUNCTIONS.get(
                    tool_call.name
                )


                if tool_function is None:

                    result = {
                        "error": f"Unknown tool: {tool_call.name}"
                    }

                else:

                    # 真正执行 Tool
                    try:

                        result = tool_function(
                            **arguments
                        )

                    except Exception as e:

                        result = {
                            "error": f"Tool execution failed: {str(e)}"
                        }


            print(f"Result: {result}")


            # Tool Result → function_call_output
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(result)
                }
            )


        # =========================
        # 把所有 Tool Results 交回 LLM
        # =========================

        response = client.responses.create(
            model="gpt-5.6-luna",

            previous_response_id=response.id,

            tools=TOOLS,

            input=tool_outputs
        )


    # 防止 Agent 无限循环
    return "Agent stopped: maximum number of steps reached."


# =========================
# 5. Test
# =========================

if __name__ == "__main__":

    question = """
    I want to invest $10,000 in Bitcoin.
    Use the current BTC price and calculate approximately
    how much BTC I can buy.
    """

    answer = run_agent(question)

    print("\n===== Final Answer =====")
    print(answer)