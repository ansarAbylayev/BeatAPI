from app.models import Beat
from sqlmodel import Session
from app.database import engine, create_db_and_tables

beats = [
    Beat(name="melody55", creator="Rasna", bpm=162, genre="rage", mood="sad"),
    Beat(name="melody68", creator="Rasna", bpm=160, genre="rage", mood="happy"),
    Beat(name="neon drift", creator="Ansar", bpm=148, genre="hyperpop", mood="happy"),
    Beat(name="slow burn", creator="Ansar", bpm=85, genre="lofi", mood="sad"),
    Beat(name="midnight tape", creator="Rasna", bpm=92, genre="lofi", mood="calm"),
    Beat(name="cold blocks", creator="Ansar", bpm=140, genre="drill", mood="dark"),
    Beat(name="glass city", creator="Rasna", bpm=128, genre="hyperpop", mood="energetic"),
]
create_db_and_tables()

with Session(engine) as session:
    for beat in beats:
        session.add(beat)
    print(len(beats))
    session.commit()