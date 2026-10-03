from fastapi import APIRouter


router = APIRouter(
    prefix="/competitors",
    tags=["Competitors"],
)


@router.get("")
async def list_competitors():
    return {
        "success": True,
        "data": [],
    }