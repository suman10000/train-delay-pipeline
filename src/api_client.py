
import logging
import time

import requests


logger = logging.getLogger(__name__)

BASE_URL = "https://api-v3.mbta.com"
ROUTE_ID = "CR-Fitchburg"


def fetch_predictions(max_attempts=3):
    """
    Fetch train predictions from MBTA.

    Retry temporary network failures and HTTP 429/5xx errors.
    Return the complete JSON response when successful.
    """

    url = f"{BASE_URL}/predictions"

    params = {
        "filter[route]": ROUTE_ID,
        "include": "schedule",
        "page[limit]": 10,
    }

    retryable_statuses = {429, 500, 502, 503, 504}

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=20,
            )

            if response.status_code in retryable_statuses:
                response.raise_for_status()

            response.raise_for_status()

            payload = response.json()

            logger.info(
                "API request succeeded on attempt %s",
                attempt,
            )

            return response.url, payload

        except requests.RequestException as error:
            logger.warning(
                "API request failed on attempt %s: %s",
                attempt,
                error,
            )

            if attempt == max_attempts:
                raise

        except ValueError as error:
            # Invalid JSON is not treated as a temporary
            # network failure, so we do not retry it.
            raise ValueError(
                "The API returned invalid JSON."
            ) from error

        # Exponential backoff: 1 second, then 2 seconds.
        time.sleep(2 ** (attempt - 1))

    raise RuntimeError("API ingestion failed unexpectedly.")
