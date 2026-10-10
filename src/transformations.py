
import json
import logging
from datetime import datetime, timezone
from pathlib import Path


logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_snapshot(file_path):
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_related_id(record, relationship_name):
    relationship = record.get("relationships", {}).get(
        relationship_name, {}
    )
    related_data = relationship.get("data")

    if isinstance(related_data, dict):
        return related_data.get("id")

    return None


def parse_timestamp(value):
    if not value:
        return None

    try:
        parsed = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc).isoformat()

    except (ValueError, AttributeError):
        return None


def transform_snapshot(file_path):
    snapshot = load_snapshot(file_path)
    payload = snapshot.get("payload", {})

    records = payload.get("data", [])
    included = payload.get("included", [])

    schedules = {
        item.get("id"): item
        for item in included
        if item.get("type") == "schedule"
    }

    ingestion_time = snapshot.get("ingested_at")
    if not ingestion_time:
        ingestion_time = datetime.now(timezone.utc).isoformat()

    rows = []

    for record in records:
        attributes = record.get("attributes", {})
        prediction_id = record.get("id")

        if not prediction_id:
            logger.warning("Skipping a record without an ID.")
            continue

        schedule_id = get_related_id(record, "schedule")
        schedule = schedules.get(schedule_id, {})
        schedule_attributes = schedule.get("attributes", {})

        arrival_time = attributes.get("arrival_time")
        departure_time = attributes.get("departure_time")

        scheduled_arrival = schedule_attributes.get("arrival_time")
        scheduled_departure = schedule_attributes.get("departure_time")

        predicted_arrival = parse_timestamp(arrival_time)
        predicted_departure = parse_timestamp(departure_time)

        scheduled_arrival = parse_timestamp(scheduled_arrival)
        scheduled_departure = parse_timestamp(scheduled_departure)

        arrival_delay_seconds = None

        if predicted_arrival and scheduled_arrival:
            predicted_dt = datetime.fromisoformat(predicted_arrival)
            scheduled_dt = datetime.fromisoformat(scheduled_arrival)

            arrival_delay_seconds = int(
                (predicted_dt - scheduled_dt).total_seconds()
            )

        rows.append({
            "prediction_id": prediction_id,
            "trip_id": get_related_id(record, "trip"),
            "stop_id": get_related_id(record, "stop"),
            "route_id": get_related_id(record, "route"),
            "schedule_id": schedule_id,
            "ingested_at": ingestion_time,
            "predicted_arrival": predicted_arrival,
            "scheduled_arrival": scheduled_arrival,
            "predicted_departure": predicted_departure,
            "scheduled_departure": scheduled_departure,
            "arrival_delay_seconds": arrival_delay_seconds,
            "prediction_status": attributes.get("status"),
            "stop_sequence": attributes.get("stop_sequence"),
        })

    return rows


def save_processed_rows(rows, source_file):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / f"{source_file.stem}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)

    logger.info("Saved %s rows to %s", len(rows), output_file)

    return output_file


def main():
    files = sorted(RAW_DIR.glob("*.json"))

    if not files:
        raise FileNotFoundError(
            "No raw snapshots found. Run ingestion first."
        )

    source_file = files[-1]
    rows = transform_snapshot(source_file)
    output_file = save_processed_rows(rows, source_file)

    print(f"Source file: {source_file}")
    print(f"Rows transformed: {len(rows)}")
    print(f"Output file: {output_file}")

    if rows:
        print("\nFirst transformed row:")
        print(json.dumps(rows[0], indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
