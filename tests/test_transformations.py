
from src.transformations import transform_snapshot


def test_transform_snapshot_calculates_predicted_delay(tmp_path):
    snapshot_file = tmp_path / "snapshot.json"

    snapshot_file.write_text(
        """
        {
          "ingested_at": "2026-10-10T12:00:00+00:00",
          "payload": {
            "data": [
              {
                "id": "prediction-1",
                "type": "prediction",
                "attributes": {
                  "arrival_time": "2026-10-10T12:10:00Z",
                  "departure_time": null,
                  "status": null,
                  "stop_sequence": 2
                },
                "relationships": {
                  "trip": {"data": {"id": "trip-1"}},
                  "stop": {"data": {"id": "stop-1"}},
                  "route": {"data": {"id": "route-1"}},
                  "schedule": {"data": {"id": "schedule-1"}}
                }
              }
            ],
            "included": [
              {
                "id": "schedule-1",
                "type": "schedule",
                "attributes": {
                  "arrival_time": "2026-10-10T12:05:00Z",
                  "departure_time": null
                }
              }
            ]
          }
        }
        """,
        encoding="utf-8",
    )

    rows = transform_snapshot(snapshot_file)

    assert len(rows) == 1
    assert rows[0]["prediction_id"] == "prediction-1"
    assert rows[0]["trip_id"] == "trip-1"
    assert rows[0]["stop_id"] == "stop-1"
    assert rows[0]["arrival_delay_seconds"] == 300
