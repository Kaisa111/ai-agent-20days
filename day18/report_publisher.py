
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone

from day18.report_schemas import ResearchReport
from day18.markdown_renderer import render_markdown
from day18.quality_gate import check_quality_gate


@dataclass
class PublishResult:
    published: bool
    file_path: str
    reasons: list[str]


def publish_report(
    report: ResearchReport,
    output_dir: str = "day18/reports",
) -> PublishResult:
    """
    Save verified reports to published/,
    and blocked reports to review/.
    """

    gate = check_quality_gate(report)

    folder_name = (
        "published" if gate.passed else "review"
    )

    output_path = Path(output_dir) / folder_name
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S_%f")

    file_path = output_path / f"rwa_report_{timestamp}.md"

    markdown = render_markdown(report)

    if not gate.passed:
        warning = (
            "> **REQUIRES REVIEW:** "
            "This report did not pass the quality gate.\n\n"
        )

        if gate.reasons:
            warning += "**Reasons:**\n\n"
            warning += "\n".join(
                f"- {reason}"
                for reason in gate.reasons
            )
            warning += "\n\n"

        markdown = warning + markdown

    file_path.write_text(
        markdown,
        encoding="utf-8",
    )

    return PublishResult(
        published=gate.passed,
        file_path=str(file_path),
        reasons=gate.reasons,
    )
