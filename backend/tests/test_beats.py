from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_count():
    response = client.get("/beats/count")
    assert response.status_code == 200

def test_get_beat_by_id():
    response = client.get("/beats/1")
    assert response.json()["id"] == 1
    assert response.status_code == 200