
from day17.market_evidence import (
    extract_market_evidence,
)


sample_data = {
    "source": "DefiLlama",
    "metric": "TVL_USD",
    "protocols": [
        {
            "name": "Protocol A",
            "tvl": 125000000.0,
        },
        {
            "name": "Protocol B",
            "tvl": 85000000.0,
        },
    ],
}


evidence_list, trusted_sources = (
    extract_market_evidence(sample_data)
)

print("Evidence count:", len(evidence_list))

for evidence in evidence_list:
    print("\nClaim:", evidence.claim)
    print("Source ID:", evidence.source_id)
    print("Evidence:", evidence.evidence_text)

print("\nTrusted source count:", len(trusted_sources))

assert len(evidence_list) == 2
assert len(trusted_sources) == 2
assert evidence_list[0].source_type == "api"
assert evidence_list[0].verification_status == "unverified"

print("\nMarket evidence extraction test passed!")
