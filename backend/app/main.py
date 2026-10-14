from fastapi import FastAPI

from app.routers import beats
from app.database import create_db_and_tables

app = FastAPI(
    title="Beat API",
    description="API for cataloging and sharing music beats",
    version="1.0.0",
)


app.include_router(beats.router)

create_db_and_tables()

@app.get("/")
def root():
    return {
        "message": "Beat API is running"
    }