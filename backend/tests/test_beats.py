



def test_get_count(client):
    response = client.get("/beats/count")
    assert response.status_code == 200

def test_get_beat_by_id(client):
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

def test_get_beat_not_found(client):
    response = client.get("/beats/999")
    assert response.json()["detail"] == "Beat not found"
    assert response.status_code == 404

def test_delete_beat_by_id(client):
    """checks that the beat was really deleted"""
    created = client.post("/beats", json = {
        "name" : "melody55",
        "creator" : "Rasna",
        "bpm" : 162,
        "genre" : "rage",
        "mood" : "sad"
    })
    beat_id = created.json()["id"]
    response=  client.delete(f"/beats/{beat_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "successfully deleted"
    after_delete = client.get(f"/beats/{beat_id}")
    assert after_delete.status_code == 404
    assert after_delete.json()["detail"] == "Beat not found"

def test_get_beats(client):
    client.post("/beats", json = {
        "name" : "melody55",
        "creator" : "Rasna",
        "bpm" : 162,
        "genre" : "rage",
        "mood" : "sad"
    })
    response = client.get("/beats/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_filter_by_genre(client):
    """creates 2 beats with different genres so the filter has something to exclude"""
    client.post("/beats", json = {
        "name" : "melody55",
        "creator" : "Rasna",
        "bpm" : 162,
        "genre" : "rage",
        "mood" : "sad"
    })
    client.post("/beats", json = {
        "name" : "melody56",
        "creator" : "Rasna",
        "bpm" : 162,
        "genre" : "lofi",
        "mood" : "sad"
    })
    response = client.get("/beats?genre=lofi")
    assert response.status_code == 200
    assert len(response.json()) > 0
    for beat in response.json():
        assert beat["genre"] == "lofi"


def test_create_beat_invalid(client):
    response = client.post("/beats", json = {
        "creator" : "Rasna",
        "bpm" : 162,
        "genre" : "rage",
        "mood" : "sad"
    })
    assert response.status_code == 422

def test_delete_beat_not_found(client):
    response = client.delete("/beats/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Beat not found"