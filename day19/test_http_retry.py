
from unittest.mock import Mock, patch

import requests

from day19.http_retry import get_json_with_retry


def main():
    # Test 1: First request fails, second succeeds.
    good_response = Mock()
    good_response.raise_for_status.return_value = None
    good_response.json.return_value = {"ok": True}

    with patch(
        "day19.http_retry.requests.Session"
    ) as session_cls, patch(
        "day19.http_retry.time.sleep"
    ) as sleep_mock:

        session = (
            session_cls.return_value
            .__enter__.return_value
        )

        session.get.side_effect = [
            requests.exceptions.SSLError(
                "Simulated TLS failure"
            ),
            good_response,
        ]

        result = get_json_with_retry(
            "https://example.com/api",
            max_attempts=3,
        )

        assert result == {"ok": True}
        assert session.get.call_count == 2
        assert sleep_mock.call_count == 1

    print("Retry recovery test passed!")

    # Test 2: HTTP 404 should not be retried.
    bad_response = Mock()
    bad_response.status_code = 404
    bad_response.raise_for_status.side_effect = (
        requests.HTTPError(
            "404 Not Found",
            response=bad_response,
        )
    )

    with patch(
        "day19.http_retry.requests.Session"
    ) as session_cls:

        session = (
            session_cls.return_value
            .__enter__.return_value
        )

        session.get.return_value = bad_response

        try:
            get_json_with_retry(
                "https://example.com/missing"
            )
        except requests.HTTPError:
            pass
        else:
            raise AssertionError(
                "Expected HTTPError"
            )

        assert session.get.call_count == 1

    print("Non-retryable error test passed!")
    print("\nHTTP retry tests passed!")


if __name__ == "__main__":
    main()
