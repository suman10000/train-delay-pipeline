
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.api_client import fetch_predictions
from src.validation import validate_payload


logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw")


def run_ingestion():
    """
    Fetch predictions, validate the response,
    and save a timestamped raw JSON snapshot.
    """

    logger.info("Starting train prediction ingestion.")

    endpoint, payload = fetch_predictions()

    records = validate_payload(payload)

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    ingestion_time = datetime.now(timezone.utc)

    filename = ingestion_time.strftime(
        "%Y%m%dT%H%M%S%fZ"
    ) + ".json"

    output_path = RAW_DIR / filename

    snapshot = {
        "source": "MBTA V3 API",
        "endpoint": endpoint,
        "ingested_at": ingestion_time.isoformat(),
        "record_count": len(records),
        "payload": payload,
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(snapshot, file, indent=2)

    logger.info("Received %s records.", len(records))
    logger.info("Saved raw snapshot to %s", output_path)

    return output_path
