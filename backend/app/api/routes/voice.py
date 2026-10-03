from fastapi import APIRouter


router = APIRouter(
    prefix="/voice",
    tags=["Voice"],
)


@router.get("/status")
async def voice_status():
    return {
        "success": True,
        "data": {
            "enabled": False,
            "provider": "mock",
        },
    }