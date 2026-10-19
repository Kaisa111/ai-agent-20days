
from day15.agents import (
    run_crypto_agent,
    run_rwa_agent,
)
from day15.parallel_research import run_research_agents
from day12.fault_tolerant_agents import safe_run_agent


def execute_research_plan(plan):
    """Execute only the agents required by the plan."""

    if plan.route == "both":
        return run_research_agents(
            crypto_question=plan.crypto_question,
            rwa_question=plan.rwa_question,
        )

    if plan.route == "crypto":
        crypto = safe_run_agent(
            "crypto",
            run_crypto_agent,
            plan.crypto_question,
        )

        return {
            "crypto": crypto,
            "rwa": None,
            "elapsed": None,
        }

    if plan.route == "rwa":
        rwa = safe_run_agent(
            "rwa",
            run_rwa_agent,
            plan.rwa_question,
        )

        return {
            "crypto": None,
            "rwa": rwa,
            "elapsed": None,
        }

    if plan.route == "other":
        return {
            "crypto": None,
            "rwa": None,
            "elapsed": None,
        }

    raise ValueError(f"Unknown route: {plan.route}")
