from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_count():
    response = client.get("/beats/count")
    assert response.status_code == 200