
from day17.market_snapshot import (
    create_market_snapshot,
    build_snapshot_registry,
)

from day17.source_registry import (
    create_source_id,
)


protocols = [
    {
        "name": "Protocol A",
        "slug": "protocol-a",
        "tvl": 125000000.0,
    },
    {
        "name": "Protocol B",
        "slug": "protocol-b",
        "tvl": 85000000.0,
    },
]


snapshot = create_market_snapshot(
    protocols
)

registry = build_snapshot_registry(
    snapshot
)

print("Snapshot ID:", snapshot.snapshot_id)
print("Retrieved at:", snapshot.retrieved_at_utc)
print("Protocol count:", len(snapshot.protocols))
print("Registry count:", len(registry))

source_id = (
    f"{snapshot.snapshot_id}:"
    f"{create_source_id(protocols[0])}"
)

assert source_id in registry
assert registry[source_id]["tvl"] == 125000000.0
assert len(registry) == 2

print("\nMarket snapshot tests passed!")
