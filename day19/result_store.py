
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from day19.evaluation_schemas import (
    AgentRunRecord,
    EvaluationSummary,
)


def save_benchmark_result(
    records: list[AgentRunRecord],
    summary: EvaluationSummary,
    output_dir: str = "day19/results",
) -> str:
    """
    Save benchmark records and summary to JSON.
    """

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S_%f")

    filename = (
        f"benchmark_{timestamp}_{uuid4().hex[:8]}.json"
    )

    output_path = directory / filename

    payload = {
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "summary": summary.model_dump(),
        "records": [
            record.model_dump()
            for record in records
        ],
    }

    with output_path.open(
        "x",
        encoding="utf-8",
    ) as file:
        json.dump(
            payload,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return str(output_path)
