print("DEBUG 1: Python started", flush=True)

from typing import TypedDict

from langgraph.graph import StateGraph, START, END

print("DEBUG 2: LangGraph imported", flush=True)

# 1. 定义 State
class AgentState(TypedDict):
    question: str
    answer: str


# 2. 定义 Node
def process_question(state: AgentState):

    question = state["question"]

    answer = f"I received your question: {question}"

    return {"answer": answer}


# 3. 创建 Graph
builder = StateGraph(AgentState)


# 4. 注册 Node
builder.add_node("process", process_question)


# 5. 定义 Edge
builder.add_edge(START, "process")
builder.add_edge("process", END)


# 6. 编译 Graph
graph = builder.compile()


# 7. 执行 Graph
if __name__ == "__main__":
    print("DEBUG 3: Main started", flush=True)

    result = graph.invoke({
        "question": "What is RWA?",
        "answer": ""
    })

    print("DEBUG 4: Graph finished", flush=True)
    print(result)