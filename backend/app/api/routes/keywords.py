from fastapi import APIRouter


router = APIRouter(
    prefix="/keywords",
    tags=["Keywords"],
)


@router.get("")
async def list_keywords():
    return {
        "success": True,
        "data": [],
    }