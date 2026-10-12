import os
from typing import TypedDict, Literal

from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from langgraph.graph import StateGraph, START, END


load_dotenv()

client = OpenAI()


# 1. 定义 LangGraph State
class AgentState(TypedDict):
    question: str
    category: str
    answer: str


# 2. 定义 LLM 结构化输出
class RouteDecision(BaseModel):
    category: Literal["crypto", "rwa", "other"]


# 3. LLM Router Node
def router_node(state: AgentState):

    question = state["question"]

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=(
            "Classify the user's question into exactly one category:\n"
            "crypto: Bitcoin, Ethereum, cryptocurrency markets, "
            "blockchain networks and related topics.\n"
            "rwa: Real World Assets, asset tokenization, "
            "tokenized bonds, tokenized credit and related topics.\n"
            "other: Questions unrelated to crypto or RWA.\n"
            "If a question involves both crypto and RWA, "
            "prefer rwa when the focus is asset tokenization."
        ),
        input=question,
        text_format=RouteDecision
    )

    decision = response.output_parsed

    if decision is None:
        raise RuntimeError("LLM did not return a valid route decision")

    category = decision.category

    print(f"[LLM Router] Category: {category}")

    return {"category": category}


# 4. Crypto Node
def crypto_node(state: AgentState):

    print("[Crypto Node] Processing...")

    return {
        "answer": "This question belongs to cryptocurrency research."
    }


# 5. RWA Node
def rwa_node(state: AgentState):

    print("[RWA Node] Processing...")

    return {
        "answer": "This question belongs to RWA research."
    }


# 6. Other Node
def other_node(state: AgentState):

    print("[Other Node] Processing...")

    return {
        "answer": "This question is outside the research scope."
    }


# 7. Conditional Edge
def route_by_category(state: AgentState):

    return state["category"]


# 8. 构建 LangGraph
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("crypto", crypto_node)
builder.add_node("rwa", rwa_node)
builder.add_node("other", other_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    route_by_category,
    {
        "crypto": "crypto",
        "rwa": "rwa",
        "other": "other"
    }
)

builder.add_edge("crypto", END)
builder.add_edge("rwa", END)
builder.add_edge("other", END)

graph = builder.compile()


# 9. 测试
if __name__ == "__main__":

    questions = [
        "Why is Ethereum important?",
        "比特币为什么有价值？",
        "What are the risks of tokenized bonds?",
        "How does tokenization of real estate work?",
        "How do I cook chicken?"
    ]

    for question in questions:

        print(f"\nQuestion: {question}")

        result = graph.invoke({
            "question": question,
            "category": "",
            "answer": ""
        })

        print("Answer:", result["answer"])