
import json
from pathlib import Path


RAW_DIR = Path("data/raw")


def main():
    files = sorted(RAW_DIR.glob("*.json"))

    if not files:
        print("No raw snapshots found. Run ingestion first.")
        return

    latest_file = files[-1]

    with latest_file.open("r", encoding="utf-8") as file:
        snapshot = json.load(file)

    payload = snapshot.get("payload", {})
    records = payload.get("data", [])
    included = payload.get("included", [])

    print(f"Snapshot: {latest_file}")
    print(f"Records: {len(records)}")
    print(f"Included resources: {len(included)}")

    if not records:
        print("No prediction records to inspect.")
        return

    print("\nFirst prediction record:")
    print(json.dumps(records[0], indent=2))

    print("\nFirst included resource:")
    if included:
        print(json.dumps(included[0], indent=2))
    else:
        print("No included resources found.")


if __name__ == "__main__":
    main()
