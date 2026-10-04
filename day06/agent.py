import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from day06.tools import (
    get_crypto_price,
    calculate_position,
    search_crypto_news
)


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


tools = [
    {
        "type": "function",
        "name": "get_crypto_price",
        "description": (
            "Get the current USD price and 24-hour percentage "
            "change for BTC, ETH, or SOL."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "enum": ["BTC", "ETH", "SOL"],
                    "description": "Cryptocurrency symbol."
                }
            },
            "required": ["symbol"],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "calculate_position",
        "description": (
            "Calculate approximately how much cryptocurrency "
            "can be purchased for a given USD investment "
            "at a given cryptocurrency price."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "investment_usd": {
                    "type": "number",
                    "description": "Amount of USD to invest."
                },
                "price_usd": {
                    "type": "number",
                    "description": "Current cryptocurrency price in USD."
                }
            },
            "required": [
                "investment_usd",
                "price_usd"
            ],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "search_crypto_news",
        "description": (
            "Search recent cryptocurrency news relevant to "
            "the user's research question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A concise search query for finding "
                        "relevant cryptocurrency news."
                    )
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
]

question = """
What is the latest Bitcoin news?
Use recent news to answer.
"""


response = client.responses.create(
    model="gpt-5.6-luna",

    instructions="""
    You are a crypto research assistant.

    Use the available news search tool when the user asks
    about recent cryptocurrency events, market movements,
    or news.

    Generate a concise and relevant search query based on
    the user's question.
    """,

    tools=tools,

    input=question
)


print(response.output)

TOOL_FUNCTIONS = {
    "get_crypto_price": get_crypto_price,
    "calculate_position": calculate_position,
    "search_crypto_news": search_crypto_news
}

def run_agent(user_message: str):

    input_items = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    max_steps = 5

    for step in range(max_steps):

        print(f"\n===== Agent Step {step + 1} =====")

        response = client.responses.create(
            model="gpt-5.6-luna",

            instructions="""
            You are a crypto research agent.

            Use tools when external data or deterministic calculations
            are required.

            Use get_crypto_price for current BTC, ETH, or SOL prices
            and 24-hour price changes.

            Use search_crypto_news for recent cryptocurrency news,
            events, and explanations of market movements.

            Use calculate_position when an exact investment position
            calculation is required.

            For questions asking why a cryptocurrency is rising or
            falling today, first verify the actual market performance
            using market data and use recent news when needed to
            investigate possible explanations.

            Do not claim that a news event caused a market movement
            unless the available evidence supports that conclusion.
            Distinguish facts from possible explanations.

            When enough information has been collected, provide a
            clear final answer.

            If a tool returns an error, do not invent missing data.
            Use another reasonable approach when possible.
            If the required information cannot be obtained, clearly
            state the limitation.            
            """,

            tools=tools,
            input=input_items
        )

        input_items += response.output

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            print("No more tool calls.")
            return response.output_text

        for tool_call in tool_calls:

            print(f"Tool: {tool_call.name}")
            print(f"Arguments: {tool_call.arguments}")


            try:
                arguments = json.loads(tool_call.arguments)

                tool_function = TOOL_FUNCTIONS.get(tool_call.name)

                if tool_function is None:
                    result = {
                        "error": f"Unknown tool: {tool_call.name}"
                    }

                else:
                    result = tool_function(**arguments)

            except json.JSONDecodeError as e:
                result = {
                    "error": f"Invalid tool arguments: {str(e)}"
                }

            except Exception as e:
                result = {
                    "error": f"Tool execution failed: {str(e)}"
                }                

            print(f"Result: {result}")

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
            )

    return "Agent stopped: maximum number of steps reached."

if __name__ == "__main__":

    
    question = """
    What is the latest Bitcoin news?
    Use recent news to answer.
    """

    answer = run_agent(question)

    print("\n===== Final Answer =====")
    print(answer)