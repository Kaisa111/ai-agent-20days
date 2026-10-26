
import hashlib
import json
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from day17.source_registry import (
    build_source_registry,
)


class MarketSnapshot(BaseModel):
    snapshot_id: str
    source: str = "DefiLlama"
    retrieved_at_utc: str
    protocols: list[dict] = Field(default_factory=list)


def create_market_snapshot(
    protocols: list[dict],
) -> MarketSnapshot:
    """
    Create a reproducible market data snapshot.

    The snapshot ID identifies this particular
    set of API records and retrieval time.
    """

    retrieved_at = datetime.now(
        timezone.utc
    ).isoformat()

    payload = {
        "source": "DefiLlama",
        "retrieved_at_utc": retrieved_at,
        "protocols": protocols,
    }

    serialized = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )

    digest = hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()[:16]

    return MarketSnapshot(
        snapshot_id=f"snapshot:{digest}",
        retrieved_at_utc=retrieved_at,
        protocols=protocols,
    )


def build_snapshot_registry(
    snapshot: MarketSnapshot,
) -> dict[str, dict]:
    """
    Create source IDs scoped to a snapshot.
    """

    protocol_registry = build_source_registry(
        snapshot.protocols
    )

    return {
        f"{snapshot.snapshot_id}:{source_id}": protocol
        for source_id, protocol in protocol_registry.items()
    }
