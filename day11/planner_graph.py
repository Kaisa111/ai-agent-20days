
from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from day11.task_planner import create_research_plan
from day09.rag_graph import graph as rwa_graph
from day10.first_tool_graph import graph as crypto_graph


# 1. 定义主图状态
class PlannerState(TypedDict):
    question: str
    route: str
    crypto_question: str
    rwa_question: str
    requires_live_data: bool
    answer: str


# 2. Planner 节点
def planner_node(state: PlannerState):

    print("[Planner] Analyzing user question...")

    plan = create_research_plan(state["question"])

    print("[Planner] Route:", plan.route)
    print("[Planner] Crypto task:", plan.crypto_question)
    print("[Planner] RWA task:", plan.rwa_question)
    print("[Planner] Live data:", plan.requires_live_data)

    return {
        "route": plan.route,
        "crypto_question": plan.crypto_question,
        "rwa_question": plan.rwa_question,
        "requires_live_data": plan.requires_live_data,
    }


# 3. Crypto 执行节点
def crypto_node(state: PlannerState):

    print("[Crypto Agent] Running...")

    result = crypto_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=state["crypto_question"]
                )
            ],
            "tool_rounds": 0,
        },
        config={"recursion_limit": 15},
    )

    return {
        "answer": result["messages"][-1].content
    }


# 4. RWA 执行节点
def rwa_node(state: PlannerState):

    print("[RWA Agent] Running...")

    result = rwa_graph.invoke({
        "question": state["rwa_question"]
    })

    return {
        "answer": result["answer"]
    }


# 5. 双 Agent 执行节点
def both_node(state: PlannerState):

    print("[Multi-Agent] Running Crypto Agent...")

    crypto_result = crypto_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=state["crypto_question"]
                )
            ],
            "tool_rounds": 0,
        },
        config={"recursion_limit": 15},
    )

    crypto_answer = crypto_result["messages"][-1].content

    print("[Multi-Agent] Running RWA Agent...")

    rwa_result = rwa_graph.invoke({
        "question": state["rwa_question"]
    })

    rwa_answer = rwa_result["answer"]

    return {
        "answer": (
            "=== Crypto Research ===\n"
            + crypto_answer
            + "\n\n=== RWA Research ===\n"
            + rwa_answer
        )
    }


# 6. 其他问题
def other_node(state: PlannerState):

    return {
        "answer": (
            "This research agent currently supports "
            "cryptocurrency and RWA-related questions."
        )
    }


# 7. 路由函数
def choose_route(state: PlannerState) -> Literal[
    "crypto", "rwa", "both", "other"
]:
    return state["route"]


# 8. 构建 LangGraph
builder = StateGraph(PlannerState)

builder.add_node("planner", planner_node)
builder.add_node("crypto", crypto_node)
builder.add_node("rwa", rwa_node)
builder.add_node("both", both_node)
builder.add_node("other", other_node)

builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    choose_route,
    {
        "crypto": "crypto",
        "rwa": "rwa",
        "both": "both",
        "other": "other",
    },
)

builder.add_edge("crypto", END)
builder.add_edge("rwa", END)
builder.add_edge("both", END)
builder.add_edge("other", END)

graph = builder.compile()


# 9. 测试入口
if __name__ == "__main__":

    question = (
        "Compare Bitcoin and tokenized Treasury bonds "
        "in terms of liquidity and custody risks."
    )

    result = graph.invoke({
        "question": question,
        "route": "",
        "crypto_question": "",
        "rwa_question": "",
        "requires_live_data": False,
        "answer": "",
    })

    print("\n=== Final Result ===")
    print("Route:", result["route"])
    print("Answer:", result["answer"])
