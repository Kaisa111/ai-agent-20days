
from day12.resilient_research import generate_report


def build_research_report(
    question: str,
    route: str,
    results: dict,
) -> str:
    """Build a report based on the selected research route."""

    if route == "both":
        return generate_report(
            question=question,
            results=results,
        )

    if route == "other":
        return (
            "# Unsupported Research Topic\n\n"
            "This research system currently supports "
            "cryptocurrency and RWA-related questions."
        )

    if route in ("crypto", "rwa"):
        result = results[route]

        if result is None:
            return (
                "# Research Failed\n\n"
                f"{route.upper()} Agent was not executed."
            )

        if result["status"] == "failed":
            return (
                "# Research Failed\n\n"
                f"{route.upper()} Agent failed: "
                f"{result['error']}"
            )

        return (
            f"# {route.upper()} Research Report\n\n"
            f"## Research Question\n{question}\n\n"
            f"## Research Findings\n{result['answer']}\n\n"
            "## Limitations\n"
            "This report covers only the requested domain. "
            "Claims without external citations have not "
            "been independently verified."
        )

    raise ValueError(f"Unknown research route: {route}")
