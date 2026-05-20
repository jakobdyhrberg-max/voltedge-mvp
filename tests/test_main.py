from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_telemetry():
    telemetry_data = {
        "charger_id": "TEST-001",
        "location": "Test Location",
        "voltage": 260,
        "current": 32,
        "power": 22,
        "temperature": 75,
        "status": "ONLINE",
        "error_code": "E500"
    }

    response = client.post("/telemetry", json=telemetry_data)

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Telemetry received"
    assert len(data["incidents_created"]) >= 1


def test_get_chargers():
    response = client.get("/chargers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_incidents():
    response = client.get("/incidents")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_alerts():
    response = client.get("/alerts")

    assert response.status_code == 200
    assert isinstance(response.json(), list)