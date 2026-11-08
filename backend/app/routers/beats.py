import uuid

from fastapi import APIRouter, HTTPException, UploadFile
from sqlmodel import select
from starlette.responses import FileResponse

from app.database import SessionDep
from app.models import Beat
from app.schemas import BeatCreate, BeatRead


router = APIRouter(
    prefix="/beats",
    tags=["beats"],
)




@router.get("/")
def get_beats(session: SessionDep, genre: str | None = None, min_bpm: int | None = None, max_bpm: int | None = None,
              mood: str | None = None ) -> list[BeatRead]:
    """Get all beats, with optional filters by genre, mood and BPM range. """
    query = select(Beat)
    if genre:
        query = query.where(Beat.genre == genre )
    if min_bpm is not None:
        # bounds are inclusive: min_bpm=140 keeps beats at exactly 140
        query = query.where(Beat.bpm >= min_bpm)
    if max_bpm is not None:
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
def get_beat(beat_id: int, session: SessionDep) -> BeatRead:
    """get one beat by its id, gives 404 if not found. """
    beat = session.get(Beat, beat_id)
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    return beat

@router.post("/", status_code=201)
def add_beat(beat: BeatCreate, session: SessionDep) -> BeatRead:
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

@router.post("/{beat_id}/upload")
def upload_file(beat_id: int, session: SessionDep, file: UploadFile) -> BeatRead:
    """upload an audiofile for a beat and store its path, 404 if not found"""
    beat = session.get(Beat, beat_id)
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    if not file.content_type.startswith("audio/") :
        raise HTTPException(status_code=400, detail="Only audio files are allowed")
    contents = file.file.read()
    if len(contents) > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")
    my_uuid = uuid.uuid4()
    names = file.filename.split(".")
    full_name = f"{my_uuid}.{names[-1]}"
    path = f"storage/originals/{full_name}"
    with open(path,"wb") as f:
        f.write(contents)
    beat.file_path = path
    session.add(beat)
    session.commit()
    session.refresh(beat)
    return beat

@router.get("/{beat_id}/download")
def download_file(beat_id: int, session: SessionDep):
    """returns audio file to play, 404 if the beat or its file is missing"""
    beat = session.get(Beat, beat_id)
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    if not beat.file_path:
        raise HTTPException(status_code=404, detail="No file uploaded in this beat")
    return FileResponse(beat.file_path)

