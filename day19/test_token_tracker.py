
from types import SimpleNamespace

from common.token_tracker import (
    start_tracking,
    record_usage,
    get_usage,
    stop_tracking,
)


def mock_response(input_tokens, output_tokens):
    """Simulate an OpenAI API response."""
    return SimpleNamespace(
        usage=SimpleNamespace(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
    )


def test_token_accumulation():
    token = start_tracking()

    try:
        # First LLM call: claim generation
        record_usage(mock_response(1200, 350))

        # Second LLM call: semantic validation
        record_usage(mock_response(800, 150))

        usage = get_usage()

        assert usage.input_tokens == 2000
        assert usage.output_tokens == 500
        assert usage.api_calls == 2

        print("Token accumulation test passed!")

    finally:
        stop_tracking(token)


def test_run_isolation():
    # First Agent run
    first_token = start_tracking()

    try:
        record_usage(mock_response(1000, 200))

        first_usage = get_usage()
        assert first_usage.input_tokens == 1000

    finally:
        stop_tracking(first_token)

    # Second Agent run
    second_token = start_tracking()

    try:
        usage = get_usage()

        assert usage.input_tokens == 0
        assert usage.output_tokens == 0
        assert usage.api_calls == 0

        record_usage(mock_response(300, 50))

        usage = get_usage()

        assert usage.input_tokens == 300
        assert usage.output_tokens == 50

        print("Run isolation test passed!")

    finally:
        stop_tracking(second_token)


def test_missing_usage():
    token = start_tracking()

    try:
        # Response without usage information
        record_usage(SimpleNamespace(usage=None))

        usage = get_usage()

        assert usage.input_tokens == 0
        assert usage.output_tokens == 0
        assert usage.api_calls == 0

        print("Missing usage test passed!")

    finally:
        stop_tracking(token)


def test_cached_token_accumulation():
    """Test cached input token tracking."""

    token = start_tracking()

    try:
        # First API call
        response1 = SimpleNamespace(
            usage=SimpleNamespace(
                input_tokens=1000,
                output_tokens=200,
                input_tokens_details=SimpleNamespace(
                    cached_tokens=600
                ),
            )
        )

        # Second API call
        response2 = SimpleNamespace(
            usage=SimpleNamespace(
                input_tokens=800,
                output_tokens=100,
                input_tokens_details=SimpleNamespace(
                    cached_tokens=300
                ),
            )
        )

        record_usage(response1)
        record_usage(response2)

        usage = get_usage()

        assert usage.input_tokens == 1800
        assert usage.output_tokens == 300
        assert usage.cached_input_tokens == 900
        assert usage.api_calls == 2

        print("Cached token accumulation test passed!")

    finally:
        stop_tracking(token)


if __name__ == "__main__":
    test_token_accumulation()
    test_run_isolation()
    test_missing_usage()
    test_cached_token_accumulation()

    print("\nAll Token Tracker tests passed!")
