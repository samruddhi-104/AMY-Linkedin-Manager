import base64
import logging
from pathlib import Path

import httpx
from openai import AsyncOpenAI

from app.config import get_settings
from app.providers.openai.exceptions import (
    OpenAIConfigurationError,
    OpenAIRequestError,
)


logger = logging.getLogger(__name__)


class OpenAIImageProvider:

    def __init__(self) -> None:

        settings = get_settings()

        if not settings.openai_api_key:

            raise OpenAIConfigurationError(
                "OPENAI_API_KEY is not configured."
            )

        self.settings = settings

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key
        )

    async def generate(
        self,
        prompt: str,
        output_path: Path,
    ) -> dict:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:

            response = (
                await self.client.images.generate(
                    model=self.settings.openai_image_model,
                    prompt=prompt,
                    size="1024x1024",
                )
            )

            image_data = response.data[0]

            # -------------------------------------------------
            # Base64 response
            # -------------------------------------------------

            if getattr(
                image_data,
                "b64_json",
                None,
            ):

                raw = base64.b64decode(
                    image_data.b64_json
                )

                output_path.write_bytes(raw)

            # -------------------------------------------------
            # URL response fallback
            # -------------------------------------------------

            elif getattr(
                image_data,
                "url",
                None,
            ):

                async with httpx.AsyncClient(
                    timeout=120
                ) as client:

                    result = await client.get(
                        image_data.url
                    )

                    result.raise_for_status()

                    output_path.write_bytes(
                        result.content
                    )

            else:

                raise OpenAIRequestError(
                    "Image provider returned no image data."
                )

            return {
                "file_path": str(
                    output_path
                ),
                "provider": "openai",
            }

        except OpenAIRequestError:
            raise

        except Exception as exc:

            logger.exception(
                "Image generation failed."
            )

            raise OpenAIRequestError(
                "Image generation failed."
            ) from exc