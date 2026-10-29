
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPricing:
    input_per_million: float
    cached_input_per_million: float
    output_per_million: float


GPT_4_1_MINI_PRICING = ModelPricing(
    input_per_million=0.40,
    cached_input_per_million=0.10,
    output_per_million=1.60,
)


def calculate_api_cost(
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int = 0,
    pricing: ModelPricing = GPT_4_1_MINI_PRICING,
) -> float:
    """
    Estimate API cost in USD.

    Assumes cached_input_tokens is included
    in input_tokens.
    """

    if (
        input_tokens < 0
        or output_tokens < 0
        or cached_input_tokens < 0
    ):
        raise ValueError(
            "Token counts cannot be negative"
        )

    if cached_input_tokens > input_tokens:
        raise ValueError(
            "Cached tokens cannot exceed input tokens"
        )

    regular_input_tokens = (
        input_tokens - cached_input_tokens
    )

    input_cost = (
        regular_input_tokens
        * pricing.input_per_million
        / 1_000_000
    )

    cached_input_cost = (
        cached_input_tokens
        * pricing.cached_input_per_million
        / 1_000_000
    )

    output_cost = (
        output_tokens
        * pricing.output_per_million
        / 1_000_000
    )

    return (
        input_cost
        + cached_input_cost
        + output_cost
    )
