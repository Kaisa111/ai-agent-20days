from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. 定义 State
class AgentState(TypedDict):
    question: str
    category: str
    answer: str


# 2. Router Node：识别问题类型
def router_node(state: AgentState):

    question = state["question"].lower()

    if "bitcoin" in question or "btc" in question:
        category = "crypto"
    else:
        category = "rwa"

    print(f"[Router] Category: {category}")

    return {"category": category}


# 3. Crypto Node
def crypto_node(state: AgentState):

    print("[Crypto Node] Processing...")

    return {
        "answer": "This is a cryptocurrency question."
    }


# 4. RWA Node
def rwa_node(state: AgentState):

    print("[RWA Node] Processing...")

    return {
        "answer": "This is an RWA question."
    }


# 5. Conditional Edge：决定下一步执行哪个节点
def route_by_category(state: AgentState):

    return state["category"]


# 6. 创建 Graph
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("crypto", crypto_node)
builder.add_node("rwa", rwa_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    route_by_category,
    {
        "crypto": "crypto",
        "rwa": "rwa"
    }
)

builder.add_edge("crypto", END)
builder.add_edge("rwa", END)

graph = builder.compile()


# 7. 测试两种问题
if __name__ == "__main__":

    questions = [
        "What is Bitcoin?",
        "What are the risks of RWA?"
    ]

    for question in questions:

        print(f"\nQuestion: {question}")

        result = graph.invoke({
            "question": question,
            "category": "",
            "answer": ""
        })

        print("Answer:", result["answer"])