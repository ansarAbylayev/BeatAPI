from sqlmodel import SQLModel, Field


class Beat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    creator: str
    bpm: int
    genre: str
    mood: str
