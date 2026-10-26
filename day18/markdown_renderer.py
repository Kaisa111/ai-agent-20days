
from day18.report_schemas import ResearchReport


def render_markdown(report: ResearchReport) -> str:
    """
    Convert a structured ResearchReport
    into a Markdown document.
    """

    lines = []

    # 1. Report title and metadata
    lines.append(f"# {report.metadata.title}")
    lines.append("")
    lines.append(f"**Research Question:** {report.metadata.question}")
    lines.append(f"**Generated At (UTC):** {report.metadata.generated_at_utc}")
    lines.append(f"**Data Source:** {report.metadata.data_source}")
    lines.append(f"**Snapshot ID:** `{report.metadata.snapshot_id}`")
    lines.append(f"**Verification Status:** {report.overall_status}")
    lines.append("")

    # 2. Executive summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(report.executive_summary)
    lines.append("")

    # 3. Research sections
    for section in report.sections:
        lines.append(f"## {section.title}")
        lines.append("")
        lines.append(section.content)
        lines.append("")

        if section.evidence_ids:
            lines.append("**Evidence References:**")
            lines.append("")

            for evidence_id in section.evidence_ids:
                lines.append(f"- `{evidence_id}`")

            lines.append("")

    # 4. Quality metrics
    lines.append("## Research Quality")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")

    quality = report.quality

    lines.append(f"| Total Claims | {quality.total_claims} |")
    lines.append(f"| Verified Claims | {quality.verified_claims} |")
    lines.append(f"| Unverified Claims | {quality.unverified_claims} |")
    lines.append(f"| Contradicted Claims | {quality.contradicted_claims} |")
    lines.append(
        f"| Evidence Coverage | {quality.evidence_coverage:.2%} |"
    )
    lines.append(
        f"| Claim Completeness | {quality.claim_completeness:.2%} |"
    )
    lines.append("")

    # 5. Limitations
    lines.append("## Limitations")
    lines.append("")

    if report.limitations:
        for limitation in report.limitations:
            lines.append(f"- {limitation}")
    else:
        lines.append("- No limitations provided.")

    lines.append("")

    return "\n".join(lines)
