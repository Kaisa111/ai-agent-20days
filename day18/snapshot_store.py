
import json
from pathlib import Path


def save_snapshot(
    snapshot: dict,
    output_dir: str = "day18/reports/snapshots",
) -> str:
    """
    Persist a market snapshot as JSON.
    """

    snapshot_id = snapshot["snapshot_id"]

    safe_id = snapshot_id.replace(":", "_")

    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = output_path / f"{safe_id}.json"

    if file_path.exists():
        existing = json.loads(
            file_path.read_text(encoding="utf-8")
        )

        if existing != snapshot:
            raise ValueError(
                "Snapshot ID collision: existing data differs."
            )

        return str(file_path)

    file_path.write_text(
        json.dumps(
            snapshot,
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    return str(file_path)
