from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from typing import Annotated
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
engine = create_engine(f"sqlite:///{BASE_DIR}/beats.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]


