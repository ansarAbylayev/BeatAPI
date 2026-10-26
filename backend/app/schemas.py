from sqlmodel import SQLModel

class BeatCreate(SQLModel):
    name: str
    creator: str
    bpm: int
    genre: str
    mood: str