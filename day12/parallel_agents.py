
import time
from concurrent.futures import ThreadPoolExecutor

from langchain_core.messages import HumanMessage

from day11.task_planner import create_research_plan
from day09.rag_graph import graph as rwa_graph
from day10.first_tool_graph import graph as crypto_graph


# 1. Crypto Agent 独立执行函数
def run_crypto_agent(question: str) -> str:

    print("[Crypto Agent] Started")

    result = crypto_graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ],
            "tool_rounds": 0,
        },
        config={"recursion_limit": 15},
    )

    print("[Crypto Agent] Finished")

    return result["messages"][-1].content


# 2. RWA Agent 独立执行函数
def run_rwa_agent(question: str) -> str:

    print("[RWA Agent] Started")

    result = rwa_graph.invoke({
        "question": question
    })

    print("[RWA Agent] Finished")

    return result["answer"]


# 3. 顺序执行
def run_sequential(
    crypto_question: str,
    rwa_question: str,
):

    start = time.perf_counter()

    crypto_answer = run_crypto_agent(crypto_question)
    rwa_answer = run_rwa_agent(rwa_question)

    elapsed = time.perf_counter() - start

    return crypto_answer, rwa_answer, elapsed


# 4. 并行执行
def run_parallel(
    crypto_question: str,
    rwa_question: str,
):

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=2) as executor:

        crypto_future = executor.submit(
            run_crypto_agent,
            crypto_question,
        )

        rwa_future = executor.submit(
            run_rwa_agent,
            rwa_question,
        )

        crypto_answer = crypto_future.result()
        rwa_answer = rwa_future.result()

    elapsed = time.perf_counter() - start

    return crypto_answer, rwa_answer, elapsed


# 5. 测试入口
if __name__ == "__main__":

    question = (
        "Compare Bitcoin and tokenized Treasury bonds "
        "in terms of liquidity and custody risks."
    )

    plan = create_research_plan(question)

    print("\n=== Research Plan ===")
    print(plan.model_dump_json(indent=2))

    if plan.route != "both":
        raise ValueError(
            f"Expected route='both', got {plan.route}"
        )

    print("\n=== Sequential Execution ===")

    seq_crypto, seq_rwa, seq_time = run_sequential(
        plan.crypto_question,
        plan.rwa_question,
    )

    print(f"Sequential time: {seq_time:.2f}s")

    print("\n=== Parallel Execution ===")

    par_crypto, par_rwa, par_time = run_parallel(
        plan.crypto_question,
        plan.rwa_question,
    )

    print(f"Parallel time: {par_time:.2f}s")

    print("\n=== Performance Comparison ===")
    print(f"Sequential: {seq_time:.2f}s")
    print(f"Parallel:   {par_time:.2f}s")

    if par_time > 0:
        print(f"Speedup:    {seq_time / par_time:.2f}x")

    print("\n=== Result Validation ===")
    print("Crypto answer exists:", bool(par_crypto.strip()))
    print("RWA answer exists:", bool(par_rwa.strip()))
