
from math import isclose

from common.cost_calculator import (
    calculate_api_cost,
    GPT_4_1_MINI_PRICING,
)


def test_regular_tokens():
    """Test regular input and output pricing."""

    cost = calculate_api_cost(
        input_tokens=319,
        output_tokens=66,
    )

    expected = 0.0002332

    assert isclose(
        cost,
        expected,
        rel_tol=1e-9,
    )

    print("Regular token cost test passed!")


def test_cached_tokens():
    """Test discounted cached input tokens."""

    cost = calculate_api_cost(
        input_tokens=1000,
        output_tokens=200,
        cached_input_tokens=600,
    )

    # 400 regular input tokens
    # 600 cached input tokens
    # 200 output tokens
    expected = (
        400 * 0.40
        + 600 * 0.10
        + 200 * 1.60
    ) / 1_000_000

    assert isclose(
        cost,
        expected,
        rel_tol=1e-9,
    )

    print("Cached token cost test passed!")


def test_invalid_tokens():
    """Reject invalid token counts."""

    try:
        calculate_api_cost(
            input_tokens=100,
            output_tokens=20,
            cached_input_tokens=200,
        )
    except ValueError:
        print("Invalid token validation test passed!")
    else:
        raise AssertionError(
            "Expected ValueError for invalid cached tokens"
        )


def test_zero_tokens():
    """Zero usage should produce zero cost."""

    cost = calculate_api_cost(
        input_tokens=0,
        output_tokens=0,
    )

    assert cost == 0.0

    print("Zero token cost test passed!")


if __name__ == "__main__":
    test_regular_tokens()
    test_cached_tokens()
    test_invalid_tokens()
    test_zero_tokens()

    print("\nAll Cost Calculator tests passed!")
