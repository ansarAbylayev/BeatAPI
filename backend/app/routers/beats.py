from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.database import SessionDep
from app.models import Beat
from app.schemas import BeatCreate


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
def get_count(session: SessionDep) -> int:
    """count the  total number of beats. """
    query = select(Beat)
    beats = session.exec(query).all()
    return len(beats)


@router.get("/genres")
def get_genres(session: SessionDep) -> list[str]:
    """Get all unique genres from the beat list."""
    query = select(Beat.genre)
    genres = session.exec(query).all()
    return list(set(genres))


@router.get("/{beat_id}")
def get_beat(beat_id: int, session: SessionDep) -> Beat:
    """get one beat by its id, gives 404 if not found. """
    beat = session.get(Beat, beat_id)
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    return beat

@router.post("/")
def add_beat(beat: BeatCreate, session: SessionDep) -> Beat:
    """Create a new beat and return it with its assigned id."""
    db_beat = Beat.model_validate(beat)
    session.add(db_beat)
    session.commit()
    session.refresh(db_beat)
    return db_beat

@router.delete("/{beat_id}")
def delete_beat(beat_id: int, session: SessionDep)-> dict:
    """deletes the beat by its id. """
    beat = session.get(Beat, beat_id)
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    session.delete(beat)
    session.commit()
    return {"message": "successfully deleted"}
