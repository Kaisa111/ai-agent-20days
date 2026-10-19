
from dotenv import load_dotenv
from openai import OpenAI

from day15.schemas import ResearchReport


load_dotenv()

client = OpenAI()


def format_research_report(
    question: str,
    markdown_report: str,
) -> ResearchReport:
    """Convert an existing report into structured data."""

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=(
            "You are a research report formatter. "
            "Convert the provided report into structured data. "
            "Do not introduce new facts, sources, or citations. "
            "Keep the original research question unchanged. "
            "The summary should capture the main conclusion. "
            "Evidence must contain only claims explicitly "
            "supported in the supplied report. "
            "Risks should describe the identified risks "
            "and important evidence limitations. "
            "Sources must contain only source identifiers "
            "explicitly present in the report, such as "
            "[Chunk 4]. "
            "Do not treat agent names as independent sources. "
            "If no valid source identifiers exist, "
            "return an empty sources list."
        ),
        input=(
            f"Original question:\n{question}\n\n"
            f"Research report:\n{markdown_report}"
        ),
        text_format=ResearchReport,
    )

    report = response.output_parsed

    if report is None:
        raise RuntimeError(
            "Failed to generate structured research report"
        )

    # Ensure the original question is preserved.
    report.question = question

    return report
