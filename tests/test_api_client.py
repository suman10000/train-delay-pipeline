
import requests
import pytest

from src.api_client import fetch_predictions


def test_api_client_returns_json(monkeypatch):
    class FakeResponse:
        status_code = 200
        url = "https://example.com/predictions"

        def raise_for_status(self):
            pass

        def json(self):
            return {"data": []}

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    url, payload = fetch_predictions()

    assert url == "https://example.com/predictions"
    assert payload == {"data": []}


def test_api_client_raises_after_retries(monkeypatch):
    calls = {"count": 0}

    def fake_get(*args, **kwargs):
        calls["count"] += 1
        raise requests.Timeout("Simulated timeout")

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr("src.api_client.time.sleep", lambda _: None)

    with pytest.raises(requests.Timeout):
        fetch_predictions(max_attempts=3)

    assert calls["count"] == 3
