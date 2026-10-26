
import hashlib
import json


def create_source_id(protocol: dict) -> str:
    """
    Create a stable source identifier.

    Prefer DefiLlama's slug when available.
    """

    slug = protocol.get("slug")

    if isinstance(slug, str) and slug.strip():
        return f"DefiLlama:protocol:{slug.strip()}"

    # Fallback: deterministic ID from protocol name
    name = protocol.get("name")

    if not isinstance(name, str) or not name.strip():
        raise ValueError(
            "Protocol must have a valid name or slug"
        )

    digest = hashlib.sha256(
        name.strip().encode("utf-8")
    ).hexdigest()[:16]

    return f"DefiLlama:protocol:{digest}"


def build_source_registry(
    protocols: list[dict],
) -> dict[str, dict]:
    """
    Map source IDs to their API records.
    """

    registry = {}

    for protocol in protocols:
        source_id = create_source_id(protocol)

        if source_id in registry:
            raise ValueError(
                f"Duplicate source ID: {source_id}"
            )

        registry[source_id] = protocol

    return registry


def validate_registered_numeric_evidence(
    evidence,
    registry: dict[str, dict],
):
    """
    Validate against the record identified
    by evidence.source_id.
    """

    from day17.numeric_validator import (
        validate_numeric_evidence,
    )

    protocol = registry.get(evidence.source_id)

    if protocol is None:
        evidence.verification_status = "unverified"
        return evidence

    return validate_numeric_evidence(
        evidence,
        protocol,
    )
