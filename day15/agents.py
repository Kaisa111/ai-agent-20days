
from langchain_core.messages import HumanMessage

from day09.rag_graph import rwa_node
from day13.mcp_tool_graph import graph as crypto_graph


def run_crypto_agent(question: str) -> str:
    """Run the real Crypto Agent with MCP tools."""

    print("\n[Day15] Starting Crypto Agent...")

    result = crypto_graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ],
            "tool_rounds": 0
        },
        config={"recursion_limit": 15},
    )

    answer = result["messages"][-1].content

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("Crypto Agent returned an empty answer")

    return answer


def run_rwa_agent(question: str) -> str:
    """Run the real RWA RAG Agent."""

    print("\n[Day15] Starting RWA Agent...")

    result = rwa_node({
        "question": question,
        "category": "rwa",
        "answer": ""
    })

    answer = result["answer"]

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("RWA Agent returned an empty answer")

    return answer
