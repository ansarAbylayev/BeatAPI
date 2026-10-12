from fastapi import APIRouter


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