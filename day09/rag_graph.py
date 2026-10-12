from typing import TypedDict, Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END

from day08.hybrid_search import hybrid_retrieve

from day09.reranker import rerank_documents


load_dotenv()
client = OpenAI()


# 1. 定义 State
class AgentState(TypedDict):
    question: str
    category: str
    answer: str


# 2. 结构化路由结果
class RouteDecision(BaseModel):
    category: Literal["crypto", "rwa", "other"]


# 3. LLM Router
def router_node(state: AgentState):

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=(
            "Classify the question into crypto, rwa, or other. "
            "Crypto includes Bitcoin, Ethereum and cryptocurrencies. "
            "RWA includes real-world asset tokenization, "
            "tokenized bonds, credit and property. "
            "If the main focus is tokenized assets, choose rwa."
        ),
        input=state["question"],
        text_format=RouteDecision
    )

    decision = response.output_parsed

    if decision is None:
        raise RuntimeError("Router failed")

    print(f"[Router] {decision.category}")

    return {"category": decision.category}


# 4. RWA RAG Node
def rwa_node(state: AgentState):

    question = state["question"]

    print("[RWA] Retrieving knowledge...")

    candidates = hybrid_retrieve(
    question,
    top_k=6
    )

    documents = rerank_documents(
        question,
        candidates,
        top_k=3
    )

    print("\n[Retrieval Results]")

    for rank, doc in enumerate(documents, start=1):
        print(
            f"Rank {rank} | "
            f"Chunk {doc['chunk_id']} | "
            f"Score {doc['score']:.4f}"
        )

    context = "\n\n".join(
        f"[Chunk {doc['chunk_id']}]\n{doc['text']}"
        for doc in documents
    )

    print("\n[Retrieved Context]")
    print(context)
    print("[End Context]\n")

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "You are an RWA research assistant. "
            "Answer using only the provided context. "
            "Cite supporting chunks, such as [Chunk 4]. "
            "If the context does not contain the answer, "
            "clearly state that the available information "
            "is insufficient. "
            "Do not invent facts."
        ),
        input=(
            f"Context:\n{context}\n\n"
            f"Question:\n{question}"
        )
    )

    return {"answer": response.output_text}


# 5. Crypto Node
def crypto_node(state: AgentState):

    print("[Crypto] Processing...")

    return {
        "answer": (
            "Crypto research is not connected yet. "
            "We will integrate the tools later."
        )
    }


# 6. Other Node
def other_node(state: AgentState):

    return {
        "answer": "This question is outside the research scope."
    }


# 7. Conditional Edge
def route_by_category(state: AgentState):

    return state["category"]


# 8. 构建 Graph
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("rwa", rwa_node)
builder.add_node("crypto", crypto_node)
builder.add_node("other", other_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    route_by_category,
    {
        "rwa": "rwa",
        "crypto": "crypto",
        "other": "other"
    }
)

builder.add_edge("rwa", END)
builder.add_edge("crypto", END)
builder.add_edge("other", END)

graph = builder.compile()


if __name__ == "__main__":

    questions = [
    "What are the liquidity risks of RWA?",
    "Does token ownership guarantee legal ownership?",
    "What is the current yield of BlackRock BUIDL?",
    "Why is Bitcoin valuable?"
]

    for question in questions:

        print(f"\nQuestion: {question}")

        result = graph.invoke({
            "question": question,
            "category": "",
            "answer": ""
        })

        print("Answer:", result["answer"])