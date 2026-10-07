from fastapi import FastAPI
from app.routers import beats


app = FastAPI(
    title="Beat API",
    description="API for cataloging and sharing music beats",
    version="1.0.0",
)


app.include_router(beats.router)


@app.get("/")
def root():
    return {
        "message": "Beat API is running"
    }