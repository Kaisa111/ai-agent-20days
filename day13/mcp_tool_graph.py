from day13.mcp_adapter import call_crypto_mcp
import json
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from openai import OpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    ToolMessage,
)

from langchain_core.tools import tool

from day05.tools import get_crypto_price, calculate_position
from day06.tools import search_crypto_news

MAX_TOOL_ROUNDS = 3

load_dotenv()
client = OpenAI()


# 1. 把 Day05 的函数包装成 LangChain Tool

@tool
def crypto_price(symbol: str) -> str:
    """Get the current market price of a cryptocurrency via MCP.

    Args:
        symbol: Cryptocurrency symbol, such as BTC, ETH or SOL.
    """
    result = call_crypto_mcp(symbol)

    return json.dumps(result, ensure_ascii=False)


@tool
def position_calculator(
    investment_usd: float,
    asset_price_usd: float
) -> str:
    """Calculate how much cryptocurrency can be purchased.

    Args:
        investment_usd: Total investment amount in USD.
        asset_price_usd: Price of one unit of the cryptocurrency in USD.
    """
    result = calculate_position(
        investment_usd=investment_usd,
        asset_price_usd=asset_price_usd
    )

    return json.dumps(result, ensure_ascii=False)

@tool
def crypto_news(query: str) -> str:
    """Search for recent cryptocurrency news.

    Args:
        query: Cryptocurrency or market topic to search for.
    """
    try:
        result = search_crypto_news(query)

        if not result:
            return json.dumps({
                "status": "no_data",
                "message": "No news data was returned."
            })

        return json.dumps({
            "status": "success",
            "data": result
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "error_type": type(e).__name__,
            "message": "News search failed."
        }, ensure_ascii=False)

tools = [
    crypto_price,
    position_calculator,
    crypto_news
]

tool_node = ToolNode(tools)

openai_tools = [
    {
        "type": "function",
        "name": "crypto_price",
        "description": "Get the current price of a cryptocurrency.",
            "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Cryptocurrency symbol, e.g. BTC",
                }
            },
            "required": ["symbol"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "position_calculator",
        "description": (
            "Calculate the quantity of cryptocurrency "
            "that can be purchased using a given USD amount "
            "and asset price. Call this after obtaining "
            "the asset price when needed."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "investment_usd": {
                    "type": "number",
                    "description": "Investment amount in USD"
                },
                "asset_price_usd": {
                    "type": "number",
                    "description": "Price per cryptocurrency unit in USD"
                }
            },
            "required": [
                "investment_usd",
                "asset_price_usd"
            ],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "crypto_news",
        "description": (
            "Search for recent cryptocurrency news. "
            "Use this tool when the user asks about "
            "recent developments, news, or market events."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "News search topic, "
                        "such as Bitcoin or Ethereum"
                    )
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    }
]

# 2. 定义消息状态
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tool_rounds: int


# 3. LLM 节点
def agent_node(state: AgentState):

    # LangChain 消息 -> OpenAI Responses API 输入
    input_messages = []

    for message in state["messages"]:

        if isinstance(message, HumanMessage):
            input_messages.append({
                "role": "user",
                "content": message.content,
            })

        elif isinstance(message, AIMessage):
            if message.tool_calls:
                for call in message.tool_calls:
                    input_messages.append({
                        "type": "function_call",
                        "call_id": call["id"],
                        "name": call["name"],
                        "arguments": json.dumps(call["args"]),
                    })
            elif message.content:
                input_messages.append({
                    "role": "assistant",
                    "content": message.content,
                })

        elif isinstance(message, ToolMessage):
            input_messages.append({
                "type": "function_call_output",
                "call_id": message.tool_call_id,
                "output": str(message.content),
            })

    tool_rounds = state.get("tool_rounds", 0)

    allow_tools = tool_rounds < MAX_TOOL_ROUNDS

    print(
        f"[Agent] Tool rounds: "
        f"{tool_rounds}/{MAX_TOOL_ROUNDS}"
    )

    # 4. 声明 OpenAI 工具
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "You are a cryptocurrency research assistant. "
            "Use tools for current prices, investment calculations, "
            "and recent cryptocurrency news. "
            "Never invent prices, news, or source links. "
            "Cite news sources when available. "
            "Distinguish facts from interpretations. "
            "If information is missing, explain the limitation. "
            "When tools are unavailable, answer only from "
            "information already obtained. "
            "Do not claim missing data has been verified."
        ),
        input=input_messages,
        tools=openai_tools if allow_tools else [],
        tool_choice="auto" if allow_tools else "none",
    )


    # 5. 解析工具调用
    tool_calls = []

    for item in response.output:
        if item.type == "function_call":
            tool_calls.append({
                "name": item.name,
                "args": json.loads(item.arguments),
                "id": item.call_id,
                "type": "tool_call",
            })

    if tool_calls:
        print("[Agent] Requesting tools:", tool_calls)

        return {
            "messages": [
                AIMessage(
                    content="",
                    tool_calls=tool_calls,
                )
            ],
            "tool_rounds": tool_rounds + 1
        }

    # 6. 没有工具调用，返回最终回答
    return {
        "messages": [
            AIMessage(content=response.output_text)
        ],
        "tool_rounds": state.get("tool_rounds", 0)
    }


# 7. 判断是否继续执行工具
def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if (
        isinstance(last_message, AIMessage)
        and last_message.tool_calls
    ):
        return "tools"

    return END


# 8. 构建 LangGraph
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "agent")

graph = builder.compile()


# 9. 测试
if __name__ == "__main__":

    question = (
        "Get the current BTC price and calculate "
        "how much BTC I can buy with $25,000."
    )

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ],
            "tool_rounds": 0
        },
        config={"recursion_limit": 15},
    )

    print("\nFinal Answer:")
    print(result["messages"][-1].content)


    print("\n=== Tool Execution Trace ===")

    executed_tools = []

    for message in result["messages"]:
        if isinstance(message, ToolMessage):
            executed_tools.append(message.name)
            print(f"Tool: {message.name}")
            print(f"Result: {message.content[:300]}")
            print("---")

    assert "crypto_price" in executed_tools, (
        "crypto_price was not executed"
    )

    assert "position_calculator" in executed_tools, (
        "position_calculator was not executed"
    )

    print("\nMCP Agent End-to-End Test PASSED")
