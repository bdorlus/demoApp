"""Tests for the status endpoint."""
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_status_endpoint_returns_ok() -> None:
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "DemoApp"}
