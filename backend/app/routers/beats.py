from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/beats",
    tags=["beats"],
)

beats = [
    {"id": 1, "name": "melody55", "creator": "Rasna", "bpm": 162, "genre": "rage", "mood": "sad"},
    {"id": 2, "name": "melody68", "creator": "Rasna", "bpm": 160, "genre": "rage", "mood": "happy"},
    {"id": 3, "name": "neon drift", "creator": "Ansar", "bpm": 148, "genre": "hyperpop", "mood": "happy"},
    {"id": 4, "name": "slow burn", "creator": "Ansar", "bpm": 85, "genre": "lofi", "mood": "sad"},
    {"id": 5, "name": "midnight tape", "creator": "Rasna", "bpm": 92, "genre": "lofi", "mood": "calm"},
    {"id": 6, "name": "cold blocks", "creator": "Ansar", "bpm": 140, "genre": "drill", "mood": "dark"},
    {"id": 7, "name": "glass city", "creator": "Rasna", "bpm": 128, "genre": "hyperpop", "mood": "energetic"},
]

@router.get("/")
def get_beats(genre : str = None, min_bpm : int = None, max_bpm: int = None):
    result = []
    for beat in beats:
        if genre and beat["genre"] != genre:
            continue
        if min_bpm and min_bpm > beat["bpm"]  :
            continue
        if max_bpm and max_bpm < beat["bpm"]  :
            continue
        result.append(beat)
    return result




@router.get("/count")
def get_count():
    return len(beats)

@router.get("/genres")
def get_genres():
    genres = set()
    for beat in beats:
        genres.add(beat["genre"])
    return list(genres)



@router.get("/{beat_id}")
def get_beat(beat_id: int):
    for beat in beats:
        if beat["id"] == beat_id:
            return beat
    raise HTTPException(status_code=404, detail= "Beat not found")



