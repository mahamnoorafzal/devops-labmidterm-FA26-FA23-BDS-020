from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200

    data = response.json()
    assert data["student_id"] == "FA23-BDS-020"
    assert data["training_rows"] >= 100
    assert 0 <= data["accuracy"] <= 1
    assert data["model_version"]
    assert data["git_sha"]


def test_predict():
    response = client.post(
        "/predict",
        json={
            "records": [
                {
                    "voltage_drift": 0.69,
                    "thermal_load": 1.19,
                    "supply_variance": -0.65,
                    "demand_spike": -0.27
                }
            ]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["predictions"]) == 1
    assert data["predictions"][0] in [0, 1]
