from day16.market_report import generate_market_report
from day11.task_planner import create_research_plan
from day16.rwa_market_agent import run_rwa_market_research


def run_planned_research(question: str) -> dict:
    print("\n[Day16] Creating research plan...")

    # Step 1: Let the Planner analyze the question
    plan = create_research_plan(question)

    print("\n=== Research Plan ===")
    print(plan.model_dump_json(indent=2))

    # Step 2: Check whether the question is RWA-related
    if plan.route not in ("rwa", "both"):
        print(
            f"[Day16] Route '{plan.route}' is not "
            "supported by this RWA research module."
        )
        return {
            "question": question,
            "plan": plan.model_dump(),
            "research": None,
        }

    # Step 3: Use Planner's live-data decision
    print(
        "\n[Day16] Live data required:",
        plan.requires_live_data,
    )

    research = run_rwa_market_research(
        question=plan.rwa_question or question,
        limit=3,
        include_live_data=plan.requires_live_data,
    )

    return {
        "question": question,
        "plan": plan.model_dump(),
        "research": research,
    }



if __name__ == "__main__":
    question = (
        "What are the top 3 RWA protocols "
        "by TVL right now?"
    )


    result = run_planned_research(question)

    print("\n=== Execution Summary ===")

    if result["research"] is not None:
        research = result["research"]

        print(
            "Live data requested:",
            research["live_data_requested"],
        )

        print(
            "Market data available:",
            research["market_data"] is not None,
        )

        print("\n=== Final Research Report ===")

        report = generate_market_report(research)

        print(report)

    else:
        print("No RWA research executed.")
