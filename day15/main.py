
from day11.task_planner import create_research_plan

from day15.schemas import ResearchRequest
from day15.research_router import execute_research_plan
from day15.report_builder import build_research_report
from day15.report_formatter import format_research_report
from day15.source_validator import validate_report_sources


def main():
    # 1. User request 
    request = ResearchRequest(
        question=(
            "What are the best techniques for "
            "growing tomatoes in a home garden?"
        ),
        depth="standard",
    )


    print("=== Research Request ===")
    print(request.model_dump_json(indent=2))

    # 2. Planner
    print("\n[Planner] Creating research plan...")
    plan = create_research_plan(request.question)

    print("\n=== Research Plan ===")
    print(plan.model_dump_json(indent=2))

    # 3. Dynamic routing
    print(f"\n[Router] Selected route: {plan.route}")

    results = execute_research_plan(plan)

    # 4. Build report
    print("\n[Report Builder] Generating report...")

    report = build_research_report(
        question=request.question,
        route=plan.route,
        results=results,
    )

    print("\n=== Final Research Report ===")
    print(report)

    # 5. Structured output
    if plan.route == "other":
        print(
            "\n[Formatter] Skipped: unsupported topic."
        )
        return

    active_results = [
        results[name]
        for name in ("crypto", "rwa")
        if results[name] is not None
    ]

    if not any(
        result["status"] == "success"
        for result in active_results
    ):
        print(
            "\n[Formatter] Skipped: no successful research."
        )
        return

    print("\n[Formatter] Creating structured report...")

    structured_report = format_research_report(
        question=request.question,
        markdown_report=report,
    )

    # 6. Validate citations
    rwa_result = results.get("rwa")

    rwa_answer = (
        rwa_result["answer"]
        if rwa_result is not None
        and rwa_result["status"] == "success"
        else ""
    )

    structured_report = validate_report_sources(
        report=structured_report,
        rwa_answer=rwa_answer,
    )

    print("\n=== Structured Research Report ===")
    print(structured_report.model_dump_json(indent=2))

    # 7. Execution summary
    print("\n=== Execution Summary ===")

    for name in ("crypto", "rwa"):
        result = results[name]

        if result is None:
            print(f"{name}: skipped")
        else:
            print(f"{name}: {result['status']}")

    if results["elapsed"] is not None:
        print(
            f"Agent execution time: "
            f"{results['elapsed']:.2f}s"
        )


if __name__ == "__main__":
    main()
