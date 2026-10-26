
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from day18.snapshot_store import save_snapshot


def main():
    snapshot = {
        "snapshot_id": "snapshot:test123",
        "retrieved_at_utc": "2026-10-27T00:00:00+00:00",
        "protocols": [
            {
                "name": "Example Protocol",
                "tvl": 1000000.0,
            }
        ],
    }

    with TemporaryDirectory() as temp_dir:
        path = save_snapshot(
            snapshot,
            output_dir=temp_dir,
        )

        print("Saved snapshot:", path)

        assert Path(path).exists()

        loaded = json.loads(
            Path(path).read_text(encoding="utf-8")
        )

        assert loaded == snapshot

        # Saving the same snapshot again is safe.
        second_path = save_snapshot(
            snapshot,
            output_dir=temp_dir,
        )

        assert second_path == path

        print("Snapshot loaded successfully.")

    print("\nSnapshot store tests passed!")


if __name__ == "__main__":
    main()
