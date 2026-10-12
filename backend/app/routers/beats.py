from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/beats",
    tags=["beats"],
)

beats = [
    {"id": 1, "name" : "melody55", "creator" : "Rasna", "bpm" : 162, "genre" :"rage", "mood" : "sad" },
    {"id": 2, "name" : "melody68", "creator" : "Rasna", "bpm" : 160, "genre" :"rage", "mood" : "happy" },
]

@router.get("/")
def get_beats():
    return beats

@router.get("/{beat_id}")
def get_beat(beat_id: int):
    for beat in beats:
        if beat["id"] == beat_id:
            return beat
    raise HTTPException(status_code=404, detail= "Beat not found")

