import json

from openai import OpenAI
from pydantic import BaseModel, Field

from common.token_tracker import record_usage


class TVLClaim(BaseModel):
    protocol_name: str
    reported_tvl_usd: float


class TVLClaimReport(BaseModel):
    claims: list[TVLClaim] = Field(
        description="TVL claims in the report"
    )


def generate_tvl_claims(
    market_data: dict,
) -> TVLClaimReport:
    """
    Generate structured TVL claims using an LLM.

    The LLM must only use supplied API data.
    """

    client = OpenAI()

    protocols = market_data.get("protocols", [])

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=(
            "You are an RWA market research assistant. "
            "Generate exactly one TVL claim for each "
            "provided protocol. "
            "Copy the protocol name and TVL value "
            "from the input. "
            "Do not invent protocols or market data. "
            "Return TVL values in USD, not millions "
            "or billions."
        ),
        input=json.dumps(
            protocols,
            ensure_ascii=False,
        ),
        text_format=TVLClaimReport,
    )

    record_usage(response)

    if response.output_parsed is None:
        raise RuntimeError(
            "LLM did not return structured claims"
        )

    return response.output_parsed
