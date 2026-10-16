
from day11.task_planner import create_research_plan
from day12.fault_tolerant_agents import (
    run_parallel_safe,
    mock_crypto_agent,
    mock_rwa_agent_failure,
)
from day12.synthesizer import synthesize_research


QUESTION = (
    "Compare Bitcoin and tokenized Treasury bonds "
    "in terms of liquidity and custody risks."
)


def build_partial_report(question, results):
    """
    Generate a deterministic partial report.
    Do not invent missing research.
    """

    sections = [
        "# Partial Research Report",
        f"Original question: {question}",
        "",
        "## Available Research",
    ]

    for name in ["crypto", "rwa"]:
        result = results[name]

        if result["status"] == "success":
            sections.append(f"### {name.upper()} Agent")
            sections.append(result["answer"])
            sections.append("")

    sections.append("## Missing Research")

    for name in ["crypto", "rwa"]:
        result = results[name]

        if result["status"] == "failed":
            sections.append(
                f"- {name.upper()} Agent failed: "
                f"{result['error']}"
            )

    sections.extend([
        "",
        "## Limitations",
        "This report is incomplete. "
        "A reliable cross-domain comparison cannot be "
        "completed without both research results.",
    ])

    return "\n".join(sections)


def generate_report(question, results):

    crypto = results["crypto"]
    rwa = results["rwa"]

    success_count = sum(
        result["status"] == "success"
        for result in [crypto, rwa]
    )

    if success_count == 0:
        return (
            "# Research Failed\n\n"
            "Both research agents failed. "
            "No reliable research report can be generated."
        )

    if success_count == 1:
        return build_partial_report(question, results)

    return synthesize_research(
        question=question,
        crypto_answer=crypto["answer"],
        rwa_answer=rwa["answer"],
    )


if __name__ == "__main__":

    print("=== Resilient Research Test ===")

    print("\n[Planner] Creating plan...")
    plan = create_research_plan(QUESTION)

    if plan.route != "both":
        raise ValueError(
            f"Expected route='both', got {plan.route}"
        )

    print("\n[Multi-Agent] Simulating RWA failure...")

    results = run_parallel_safe(
        crypto_question=plan.crypto_question,
        rwa_question=plan.rwa_question,
        crypto_func=mock_crypto_agent,
        rwa_func=mock_rwa_agent_failure,
    )

    print("\n=== Agent Status ===")

    for name in ["crypto", "rwa"]:
        print(
            f"{name}: {results[name]['status']}"
        )

    report = generate_report(
        question=QUESTION,
        results=results,
    )

    print("\n=== Final Report ===")
    print(report)

    assert results["crypto"]["status"] == "success"
    assert results["rwa"]["status"] == "failed"
    assert "Partial Research Report" in report
    assert "Bitcoin custody" in report
    assert "RWA Agent failed" in report

    print("\nEND-TO-END FAULT TOLERANCE TEST PASSED")
