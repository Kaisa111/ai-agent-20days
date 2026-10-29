
import random
import time

import requests


RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def get_json_with_retry(
    url: str,
    *,
    proxies: dict | None = None,
    max_attempts: int = 3,
    timeout: tuple = (10, 20),
    backoff_factor: float = 1.0,
):
    """
    Fetch JSON with retries for transient network errors.
    """

    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    for attempt in range(1, max_attempts + 1):
        try:
            with requests.Session() as session:
                session.trust_env = proxies is None

                response = session.get(
                    url,
                    proxies=proxies,
                    timeout=timeout,
                )

                response.raise_for_status()
                return response.json()

        except requests.HTTPError as exc:
            status = (
                exc.response.status_code
                if exc.response is not None
                else None
            )

            if status not in RETRYABLE_STATUS_CODES:
                raise

            error = exc

        except (
            requests.ConnectionError,
            requests.Timeout,
        ) as exc:
            error = exc

        if attempt == max_attempts:
            raise error

        delay = (
            backoff_factor * (2 ** (attempt - 1))
            + random.uniform(0, 0.25)
        )

        print(
            f"[HTTP Retry] Attempt {attempt} failed. "
            f"Retrying in {delay:.2f}s..."
        )

        time.sleep(delay)
