from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent


class Settings(BaseSettings):
    app_name: str = "CTons AMY"
    app_env: str = "development"
    debug: bool = True

    mock_mode: bool = True

    database_url: str = "postgresql+psycopg://amy:amy@localhost:5432/ctons_amy"

    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6"
    openai_reasoning_model: str = "gpt-5.6"
    openai_image_model: str = "gpt-image-2"

    linkedin_client_id: str | None = None
    linkedin_client_secret: str | None = None
    linkedin_redirect_uri: str = "http://localhost:8000/api/linkedin/oauth/callback"
    linkedin_api_version: str = ""

    storage_path: Path = PROJECT_ROOT / "storage"
    log_level: str = "INFO"

    timezone: str = "Asia/Kolkata"

    wake_word_provider: str = "mock"
    stt_provider: str = "mock"
    tts_provider: str = "mock"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    task_default_timeout_seconds: int = 120
    task_max_retries: int = 3

    linkedin_access_token: str | None = None
    linkedin_author_urn: str | None = None
    linkedin_api_version: str = ""

    
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",

    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    settings.storage_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return settings
