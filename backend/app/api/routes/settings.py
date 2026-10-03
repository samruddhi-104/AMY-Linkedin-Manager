from fastapi import APIRouter

from app.config import get_settings


router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get("")
async def settings():
    config = get_settings()

    return {
        "success": True,
        "data": {
            "app_name": config.app_name,
            "app_env": config.app_env,
            "mock_mode": config.mock_mode,
            "timezone": config.timezone,
            "wake_word_provider": config.wake_word_provider,
            "stt_provider": config.stt_provider,
            "tts_provider": config.tts_provider,
        },
    }