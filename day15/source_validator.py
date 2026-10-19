
import re

from day15.schemas import ResearchReport


def extract_chunk_ids(text: str) -> set[int]:
    """Extract citations in the exact [Chunk N] format."""
    return {
        int(chunk_id)
        for chunk_id in re.findall(
            r"\[Chunk\s+(\d+)\]",
            text,
        )
    }


def validate_report_sources(
    report: ResearchReport,
    rwa_answer: str,
) -> ResearchReport:
    """Normalize citations against the RWA Agent answer."""

    allowed_ids = extract_chunk_ids(rwa_answer)

    # Collect citations actually used in the report.
    report_text = "\n".join(
        report.evidence + report.sources
    )
    reported_ids = extract_chunk_ids(report_text)

    valid_ids = sorted(allowed_ids & reported_ids)

    report.sources = [
        f"[Chunk {chunk_id}]"
        for chunk_id in valid_ids
    ]

    return report
