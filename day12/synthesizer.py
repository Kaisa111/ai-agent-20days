
from dotenv import load_dotenv
from openai import OpenAI

from day11.task_planner import create_research_plan
from day12.parallel_agents import run_parallel
from day12.citation_validator import validate_citations


load_dotenv()

client = OpenAI()


def synthesize_research(
    question: str,
    crypto_answer: str,
    rwa_answer: str,
) -> str:

    response = client.responses.create(
        model="gpt-4.1-mini",


        instructions=(
            "You are an evidence-grounded research synthesizer. "
            "Combine two independent research reports into a "
            "single comparative analysis. "

            "Follow these strict evidence rules: "

            "1. Use only information contained in the supplied reports. "
            "Do not introduce new facts, figures, or sources. "

            "2. Clearly distinguish between: "
            "SUPPORTED CLAIMS: statements backed by explicit evidence "
            "in the supplied reports; "
            "UNVERIFIED CLAIMS: statements without traceable evidence; "
            "INFERENCES: analytical conclusions derived from the reports. "

            "3. Preserve original source references such as [Chunk 4] "
            "and [Chunk 6] when they support a claim. "
            "Never invent citations. "
            "A source reference must support the specific statement "
            "to which it is attached. "

            "4. A statement made by an agent without a verifiable "
            "source must not be presented as independently verified. "

            "5. If the evidence does not support a definitive comparison, "
            "explicitly state that the conclusion is uncertain. "

            "6. Do not treat missing evidence as evidence of absence. "

            "7. Do not simply concatenate the two reports. "
            "Compare them along the dimensions requested by the user. "

            "Produce the following sections: "
            "1. Executive Summary; "
            "2. Evidence-Aware Comparison Table "
            "(Dimension, Bitcoin, Tokenized Treasury Bonds, Evidence Status); "
            "3. Key Trade-offs; "
            "4. Evidence Gaps; "
            "5. Provisional Conclusion. "

            "In the Evidence Status column, distinguish between "
            "'Source-supported', 'Agent-reported but unverified', "
            "and 'Insufficient evidence'. "

            "Use exact citation format [Chunk N] when citing RWA sources. "
            "Do not rewrite citations into forms such as "
            "'[RWA Agent Report, Chunk 4]' or '[Chunks 4, 6]'. "
            "Do not cite 'Crypto Agent Report' as independently verified evidence. "
            "Treat uncited Crypto Agent claims as agent-reported but unverified. "
        ),

        input=(
            f"Original question:\n{question}\n\n"
            f"=== Crypto Agent Report ===\n{crypto_answer}\n\n"
            f"=== RWA Agent Report ===\n{rwa_answer}"
        ),
    )

    return response.output_text


if __name__ == "__main__":

    question = (
        "Compare Bitcoin and tokenized Treasury bonds "
        "in terms of liquidity and custody risks."
    )

    print("[Planner] Creating research plan...")

    plan = create_research_plan(question)

    if plan.route != "both":
        raise ValueError(
            f"Expected route='both', got {plan.route}"
        )

    print("[Multi-Agent] Running parallel research...")

    crypto_answer, rwa_answer, elapsed = run_parallel(
        plan.crypto_question,
        plan.rwa_question,
    )

    print(f"\nResearch time: {elapsed:.2f}s")

    print("\n[Synthesizer] Combining research results...")

    final_report = synthesize_research(
        question=question,
        crypto_answer=crypto_answer,
        rwa_answer=rwa_answer,
    )

    print("\n=== Final Research Report ===")
    print(final_report)

    print("\n=== Citation Validation ===")

    validation = validate_citations(
        source_report=rwa_answer,
        final_report=final_report,
    )

    for key, value in validation.items():
        print(f"{key}: {value}")