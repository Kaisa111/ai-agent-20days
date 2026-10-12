from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from day09.rag_graph import graph as rwa_graph
from day10.first_tool_graph import graph as crypto_graph


class UnifiedState(TypedDict):
    question: str
    route: str
    answer: str


def router_node(state: UnifiedState):

    question = state["question"].lower()

    crypto_keywords = [
        "btc", "bitcoin", "eth", "ethereum",
        "比特币", "以太坊", "币价", "加密货币"
    ]

    rwa_keywords = [
        "rwa", "tokenization", "tokenized",
        "代币化", "资产上链", "流动性风险"
    ]

    has_crypto = any(word in question for word in crypto_keywords)
    has_rwa = any(word in question for word in rwa_keywords)

    if has_crypto and has_rwa:
        route = "both"
    elif has_rwa:
        route = "rwa"
    elif has_crypto:
        route = "crypto"
    else:
        route = "other"

    return {"route": route}


def crypto_node(state: UnifiedState):

    result = crypto_graph.invoke(
        {
            "messages": [
                HumanMessage(content=state["question"])
            ],
            "tool_rounds": 0,
        },
        config={"recursion_limit": 15},
    )

    return {
        "answer": result["messages"][-1].content
    }


def rwa_node(state: UnifiedState):

    result = rwa_graph.invoke(
        {
            "question": state["question"]
        }
    )

    return {
        "answer": result["answer"]
    }


def other_node(state: UnifiedState):

    return {
        "answer": (
            "This research agent currently supports "
            "cryptocurrency and RWA-related questions."
        )
    }


def both_node(state: UnifiedState):

    print("[Multi-Agent] Decomposing the task...")

    # 当前先使用固定子任务验证协作流程
    crypto_question = (
        "What are the main investment risks of Bitcoin?"
    )

    rwa_question = (
        "What are the liquidity risks of RWA tokenization?"
    )

    # 1. 执行 Crypto Agent
    print("[Multi-Agent] Running Crypto Agent...")

    crypto_result = crypto_graph.invoke(
        {
            "messages": [
                HumanMessage(content=crypto_question)
            ],
            "tool_rounds": 0,
        },
        config={"recursion_limit": 15},
    )

    crypto_answer = crypto_result["messages"][-1].content

    # 2. 执行 RWA Agent
    print("[Multi-Agent] Running RWA Agent...")

    rwa_result = rwa_graph.invoke({
        "question": rwa_question
    })

    rwa_answer = rwa_result["answer"]

    # 3. 合并结果
    combined_answer = (
        "=== Crypto Research ===\n"
        + crypto_answer
        + "\n\n=== RWA Research ===\n"
        + rwa_answer
    )

    return {
        "answer": combined_answer
    }

def choose_route(state: UnifiedState) -> Literal[
    "crypto", "rwa", "other", "both"
]:
    return state["route"]


builder = StateGraph(UnifiedState)

builder.add_node("router", router_node)
builder.add_node("crypto", crypto_node)
builder.add_node("rwa", rwa_node)
builder.add_node("other", other_node)
builder.add_node("both", both_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "crypto": "crypto",
        "rwa": "rwa",
        "other": "other",
        "both": "both",
    },
)

builder.add_edge("crypto", END)
builder.add_edge("rwa", END)
builder.add_edge("other", END)
builder.add_edge("both", END)

graph = builder.compile()


if __name__ == "__main__":

    question = (
        "Compare Bitcoin investment risks "
        "with RWA tokenization liquidity risks."
    )

    result = graph.invoke({
        "question": question,
        "route": "",
        "answer": "",
    })

    print("Route:", result["route"])
    print("Answer:", result["answer"])