
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests


# API endpoint and route we want to inspect
BASE_URL = "https://api-v3.mbta.com"
ROUTE_ID = "CR-Fitchburg"

# Folder where raw API responses will be saved
OUTPUT_DIR = Path("data/raw")


def fetch_predictions():
    """Fetch train predictions from the MBTA API."""

    url = f"{BASE_URL}/predictions"

    params = {
        "filter[route]": ROUTE_ID,
        "include": "schedule",
        "page[limit]": 10,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20,
        )

        # Raise an error if the API returns an HTTP failure
        response.raise_for_status()

        # Convert the JSON response into Python objects
        payload = response.json()

    except requests.RequestException as error:
        print(f"API request failed: {error}")
        sys.exit(1)

    except ValueError as error:
        print(f"Could not decode JSON: {error}")
        sys.exit(1)

    # Check that the API returned the expected structure
    if not isinstance(payload, dict):
        print("Unexpected response: expected a JSON object.")
        sys.exit(1)

    records = payload.get("data", [])

    if not isinstance(records, list):
        print("Unexpected response: 'data' is not a list.")
        sys.exit(1)

    return response.url, payload, records


def save_raw_snapshot(url, payload, records):
    """Save the original API response with ingestion metadata."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ingestion_time = datetime.now(timezone.utc)

    filename = ingestion_time.strftime(
        "%Y%m%dT%H%M%SZ"
    ) + ".json"

    output_path = OUTPUT_DIR / filename

    snapshot = {
        "source": "MBTA V3 API",
        "endpoint": url,
        "ingested_at": ingestion_time.isoformat(),
        "record_count": len(records),
        "payload": payload,
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(snapshot, file, indent=2)

    return output_path


def main():
    print("Fetching train predictions...")

    url, payload, records = fetch_predictions()

    print(f"API endpoint: {url}")
    print(f"Records received: {len(records)}")

    output_path = save_raw_snapshot(
        url,
        payload,
        records,
    )

    print(f"Raw snapshot saved to: {output_path}")

    if records:
        print("\nFirst prediction record:")
        print(json.dumps(records[0], indent=2))

        attributes = records[0].get("attributes", {})

        print("\nAvailable attribute fields:")
        print(sorted(attributes.keys()))

        print("\nSchedule relationship:")
        print(
            json.dumps(
                records[0].get("relationships", {}).get(
                    "schedule"
                ),
                indent=2,
            )
        )
    else:
        print(
            "No predictions returned. "
            "Check the route, endpoint and current service data."
        )


if __name__ == "__main__":
    main()
