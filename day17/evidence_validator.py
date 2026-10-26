
import re

from day17.schemas import ResearchEvidence


def normalize_text(text: str) -> str:
    """Normalize text for simple comparisons."""
    return " ".join(
        re.findall(r"[a-z0-9]+", text.lower())
    )


def remove_negation(text: str) -> str:
    """Remove simple English negation tokens."""
    return re.sub(
        r"\b(?:do not|does not|did not|not)\b",
        "",
        text,
        flags=re.IGNORECASE,
    )


def has_negation(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:do not|does not|did not|not)\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def validate_evidence(
    evidence: ResearchEvidence,
    trusted_sources: dict[str, str],
) -> ResearchEvidence:
    """
    Conservative rule-based evidence validation.

    This is not a general semantic fact-checker.
    """

    evidence.verification_status = "unverified"

    # Step 1: Verify source existence
    source_text = trusted_sources.get(
        evidence.source_id
    )

    if source_text is None:
        return evidence

    # Step 2: Verify evidence is in source
    quoted_text = evidence.evidence_text.strip()

    if not quoted_text:
        return evidence

    if quoted_text.lower() not in source_text.lower():
        return evidence

    # Step 3: Normalize claim and evidence
    claim = normalize_text(evidence.claim)
    quote = normalize_text(quoted_text)

    # Exact textual agreement
    if claim == quote:
        evidence.verification_status = "verified"
        return evidence

    # Step 4: Detect simple negation conflicts
    claim_without_negation = normalize_text(
        remove_negation(evidence.claim)
    )

    quote_without_negation = normalize_text(
        remove_negation(quoted_text)
    )

    if (
        claim_without_negation == quote_without_negation
        and has_negation(evidence.claim)
        != has_negation(quoted_text)
    ):
        evidence.verification_status = "contradicted"
        return evidence

    # Step 5: Other cases require deeper validation
    return evidence
