
import pytest

from src.validation import validate_payload


def test_valid_payload():
    payload = {
        "data": [
            {
                "id": "prediction-1",
                "attributes": {
                    "arrival_time": "2026-10-10T12:00:00Z"
                },
            }
        ]
    }

    records = validate_payload(payload)

    assert len(records) == 1
    assert records[0]["id"] == "prediction-1"


def test_empty_payload_is_valid():
    payload = {"data": []}

    assert validate_payload(payload) == []


def test_missing_data_field():
    with pytest.raises(ValueError):
        validate_payload({"included": []})


def test_data_must_be_a_list():
    with pytest.raises(ValueError):
        validate_payload({"data": {}})


def test_record_must_have_id():
    payload = {
        "data": [
            {"attributes": {}}
        ]
    }

    with pytest.raises(ValueError):
        validate_payload(payload)


def test_attributes_must_be_an_object():
    payload = {
        "data": [
            {"id": "prediction-1", "attributes": []}
        ]
    }

    with pytest.raises(ValueError):
        validate_payload(payload)
