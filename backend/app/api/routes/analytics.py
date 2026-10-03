from fastapi import APIRouter

from app.services.in_memory_store import store


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("")
async def analytics():

    return {
        "success": True,
        "data": {
            "available": False,
            "message": (
                "LinkedIn analytics data is "
                "not yet connected."
            ),
            "records": store.list_analytics(),
        },
    }