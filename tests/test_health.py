"""Pruebas básicas de disponibilidad de la aplicación FastAPI."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    """El endpoint de salud debe responder HTTP 200 y estado ok."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
