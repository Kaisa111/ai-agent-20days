
import time
from concurrent.futures import ThreadPoolExecutor

from day12.parallel_agents import (
    run_crypto_agent,
    run_rwa_agent,
)


def safe_run_agent(agent_name, agent_func, question):
    """
    Execute an agent safely.
    Always return a structured result.
    """

    try:
        answer = agent_func(question)

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Agent returned an empty answer")

        return {
            "agent": agent_name,
            "status": "success",
            "answer": answer,
            "error": None,
        }

    except Exception as exc:

        print(f"[{agent_name}] Failed: {type(exc).__name__}")

        return {
            "agent": agent_name,
            "status": "failed",
            "answer": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def run_parallel_safe(
    crypto_question,
    rwa_question,
    crypto_func=run_crypto_agent,
    rwa_func=run_rwa_agent,
):

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=2) as executor:

        crypto_future = executor.submit(
            safe_run_agent,
            "crypto",
            crypto_func,
            crypto_question,
        )

        rwa_future = executor.submit(
            safe_run_agent,
            "rwa",
            rwa_func,
            rwa_question,
        )

        crypto_result = crypto_future.result()
        rwa_result = rwa_future.result()

    elapsed = time.perf_counter() - start

    results = {
        "crypto": crypto_result,
        "rwa": rwa_result,
        "elapsed": elapsed,
    }

    return results


# Simulate an agent failure without calling an API.
def mock_crypto_agent(question):
    return "Bitcoin custody requires secure private key management."


def mock_rwa_agent_failure(question):
    raise TimeoutError("Simulated API timeout")


if __name__ == "__main__":

    print("=== Fault Tolerance Test ===")

    result = run_parallel_safe(
        crypto_question="Explain Bitcoin custody risks.",
        rwa_question="Explain tokenized Treasury custody risks.",
        crypto_func=mock_crypto_agent,
        rwa_func=mock_rwa_agent_failure,
    )

    print("\n=== Results ===")

    for name in ["crypto", "rwa"]:
        agent_result = result[name]

        print(f"\nAgent: {name}")
        print(f"Status: {agent_result['status']}")
        print(f"Answer: {agent_result['answer']}")
        print(f"Error: {agent_result['error']}")

    print(f"\nElapsed: {result['elapsed']:.2f}s")

    assert result["crypto"]["status"] == "success"
    assert result["rwa"]["status"] == "failed"
    assert result["crypto"]["answer"]
    assert result["rwa"]["answer"] == ""

    print("\nFault tolerance test PASSED")
