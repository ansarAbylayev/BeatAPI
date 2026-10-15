from fastapi import APIRouter, HTTPException, Depends, FastAPI, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.database import SessionDep
from app.models import Beat


router = APIRouter(
    prefix="/beats",
    tags=["beats"],
)




@router.get("/")
def get_beats(session: SessionDep, genre: str | None = None, min_bpm: int | None = None, max_bpm: int | None = None,
              mood: str | None = None ) -> list[Beat]:
    """Get all beats, with optional filters by genre, mood and BPM range. """
    query = select(Beat)
    if genre:
        query = query.where(Beat.genre == genre )
    if min_bpm:
        # bounds are inclusive: min_bpm=140 keeps beats at exactly 140
        query = query.where(Beat.bpm >= min_bpm)
    if max_bpm:
        query = query.where(Beat.bpm <= max_bpm)
    if mood:
        query = query.where(Beat.mood == mood )
    beats = session.exec(query).all()
    return beats


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
