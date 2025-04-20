from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in ["ok", "degraded"]


def test_mms_endpoint_invalid_pair():
    response = client.get(
        "/INVALID/mms", params={"from_ts": 123456, "to_ts": 123999, "range_days": 20}
    )
    assert response.status_code == 400
    assert "Invalid 'pair'" in response.text


def test_mms_endpoint_invalid_timestamp():
    response = client.get(
        "/INVALID/mms", params={"from_ts": 99999, "to_ts": 888, "range_days": 20}
    )
    assert response.status_code == 400
    assert "Invalid 'pair'" in response.text
