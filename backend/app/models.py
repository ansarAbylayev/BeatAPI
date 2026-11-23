from sqlmodel import SQLModel, Field


class Beat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    creator: str
    bpm: int
    genre: str
    mood: str
    file_path: str  | None = Field(default=None)
    preview_path: str | None = Field(default=None)

class User(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str