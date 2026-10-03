from fastapi import APIRouter

from app.config import get_settings


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health():

    settings = get_settings()

    return {
        "success": True,
        "data": {
            "status": "healthy",
            "services": {
                "database": "disabled_for_now",
                "openai": (
                    "configured"
                    if settings.openai_api_key
                    else "mock"
                ),
                "linkedin": "disabled_for_now",
                "voice": "disabled_for_now",
                "scheduler": "disabled_for_now",
            },
            "storage": "in_memory",
            "mock_mode": settings.mock_mode,
        },
    }