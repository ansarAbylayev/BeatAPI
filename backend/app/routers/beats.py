from fastapi import APIRouter, HTTPException, Depends, FastAPI, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.database import SessionDep
from app.models import Beat


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
def get_beats(genre: str | None = None, min_bpm: int | None = None, max_bpm: int | None = None,
              mood: str | None = None):
    """Get all beats, with optional filters by genre, mood and BPM range. """
    result = []
    for beat in beats:
        if genre and beat["genre"] != genre:
            continue
        # bounds are inclusive: min_bpm=140 keeps beats at exactly 140
        if min_bpm and min_bpm > beat["bpm"]:
            continue
        if max_bpm and max_bpm < beat["bpm"]:
            continue
        if mood and beat["mood"] != mood:
            continue
        result.append(beat)
    return result


@router.get("/count")
def get_count():
    """count the  total number of beats. """
    return len(beats)


@router.get("/genres")
def get_genres():
    """Get all unique genres from the beat list."""
    genres = set()
    for beat in beats:
        genres.add(beat["genre"])
    return list(genres)


@router.get("/{beat_id}")
def get_beat(beat_id: int, session: SessionDep) -> Beat:
    """get one beat by its id, gives 404 if not found. """
    beat = session.get(Beat, beat_id)
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    return beat
