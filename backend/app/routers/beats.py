from fastapi import APIRouter


router = APIRouter(
    prefix="/beats",
    tags=["beats"],
)


@router.get("/")
def get_beats():
    return []