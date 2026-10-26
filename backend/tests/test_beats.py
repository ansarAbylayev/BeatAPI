from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import create_engine,  SQLModel, Session
from app.database import get_session

client = TestClient(app)

test_engine = create_engine("sqlite:///test.db")
SQLModel.metadata.create_all(test_engine)
def get_test_session():
    with Session(test_engine) as session:
        yield session
app.dependency_overrides[get_session] = get_test_session



def test_get_count():
    response = client.get("/beats/count")
    assert response.status_code == 200

def test_get_beat_by_id():
    created = client.post("/beats", json = {
        "name" : "melody55",
        "creator" : "Rasna",
        "bpm" : 162,
        "genre" : "rage",
        "mood" : "sad"
    })
    beat_id = created.json()["id"]
    response=  client.get(f"/beats/{beat_id}")
    assert response.status_code == 200
    assert response.json()["id"] == beat_id

def test_get_beat_not_found():
    response = client.get("/beats/999")
    assert response.json()["detail"] == "Beat not found"
    assert response.status_code == 404