
from day16.rwa_data import get_rwa_protocols
from day17.schemas import ResearchEvidence
from day17.numeric_validator import validate_numeric_evidence


def main():
    # Step 1: Fetch real DefiLlama data
    protocols = get_rwa_protocols(limit=3)

    print("Fetched protocols:", len(protocols))

    if not protocols:
        raise RuntimeError("No RWA protocols returned")

    # Step 2: Select the first protocol
    protocol = protocols[0]

    name = protocol["name"]
    tvl = protocol["tvl"]

    print("Protocol:", name)
    print("TVL (USD):", f"{tvl:,.2f}")

    # Step 3: Create a correct claim
    correct_evidence = ResearchEvidence(
        claim=(
            f"{name} has a reported TVL "
            f"of ${tvl:,.2f} USD."
        ),
        source_type="api",
        source_id="DefiLlama:live:1",
        evidence_text=(
            f"Protocol: {name}; "
            f"TVL_USD: {tvl:,.2f}; "
            "Source: DefiLlama"
        ),
    )

    correct_result = validate_numeric_evidence(
        correct_evidence,
        protocol,
    )

    print(
        "Correct claim:",
        correct_result.verification_status,
    )

    assert correct_result.verification_status == "verified"

    # Step 4: Simulate a numerical hallucination
    wrong_evidence = ResearchEvidence(
        claim=(
            f"{name} has a reported TVL "
            f"of ${tvl * 10:,.2f} USD."
        ),
        source_type="api",
        source_id="DefiLlama:live:1",
        evidence_text=correct_evidence.evidence_text,
    )

    wrong_result = validate_numeric_evidence(
        wrong_evidence,
        protocol,
    )

    print(
        "Incorrect claim:",
        wrong_result.verification_status,
    )

    assert wrong_result.verification_status == "contradicted"

    print("\nLive numeric validation test passed!")


if __name__ == "__main__":
    main()
