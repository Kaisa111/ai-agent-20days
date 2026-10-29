
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    api_calls: int = 0


_current_usage: ContextVar[TokenUsage | None] = (
    ContextVar("current_token_usage", default=None)
)


def start_tracking():
    """Start a new independent tracking scope."""
    return _current_usage.set(TokenUsage())


def record_usage(response) -> None:
    """Record token usage from an OpenAI response."""
    current = _current_usage.get()

    if current is None:
        return

    usage = getattr(response, "usage", None)

    if usage is None:
        return

    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens

    input_details = getattr(
        usage, "input_tokens_details", None
    )

    cached_tokens = (
        getattr(input_details, "cached_tokens", 0) or 0
    )

    updated = TokenUsage(
        input_tokens=(
            current.input_tokens + input_tokens
        ),
        output_tokens=(
            current.output_tokens + output_tokens
        ),
        cached_input_tokens=(
            current.cached_input_tokens + cached_tokens
        ),
        api_calls=current.api_calls + 1,
    )

    _current_usage.set(updated)


def get_usage() -> TokenUsage | None:
    """Get usage for the current tracking scope."""
    return _current_usage.get()


def stop_tracking(token) -> None:
    """Restore the previous tracking scope."""
    _current_usage.reset(token)
