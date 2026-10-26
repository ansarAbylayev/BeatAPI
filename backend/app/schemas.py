from sqlmodel import SQLModel

class BeatBase(SQLModel):
    name: str
    creator: str
    bpm: int
    genre: str
    mood: str

class BeatCreate(BeatBase):
    pass

class BeatRead(BeatBase):
    id: int
