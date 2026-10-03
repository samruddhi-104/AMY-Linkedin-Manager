import json
import logging
from typing import Any

from openai import AsyncOpenAI

from app.config import get_settings
from app.providers.openai.exceptions import (
    OpenAIConfigurationError,
    OpenAIRequestError,
)


logger = logging.getLogger(__name__)


class OpenAIProvider:
    """
    Centralized OpenAI provider.

    All OpenAI-specific code should remain here rather
    than being scattered throughout the agents.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

        if not self.settings.openai_api_key:
            raise OpenAIConfigurationError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = AsyncOpenAI(
            api_key=self.settings.openai_api_key
        )

    async def generate_text(
        self,
        *,
        instructions: str,
        input_text: str,
        model: str | None = None,
        use_web_search: bool = False,
    ) -> dict[str, Any]:

        selected_model = (
            model or self.settings.openai_model
        )

        tools: list[dict[str, Any]] = []

        if use_web_search:
            tools.append(
                {
                    "type": "web_search",
                }
            )

        try:
            response = await self.client.responses.create(
                model=selected_model,
                instructions=instructions,
                input=input_text,
                tools=tools or None,
            )

        except Exception as exc:
            logger.exception(
                "OpenAI request failed."
            )

            raise OpenAIRequestError(
                "OpenAI request failed."
            ) from exc

        return {
            "response_id": response.id,
            "text": response.output_text,
            "raw": response,
        }

    async def generate_json(
        self,
        *,
        instructions: str,
        input_text: str,
        schema_name: str,
        schema: dict[str, Any],
        model: str | None = None,
        use_web_search: bool = False,
    ) -> dict[str, Any]:

        selected_model = (
            model or self.settings.openai_model
        )

        tools: list[dict[str, Any]] = []

        if use_web_search:
            tools.append(
                {
                    "type": "web_search",
                }
            )

        try:
            response = await self.client.responses.create(
                model=selected_model,
                instructions=instructions,
                input=input_text,
                tools=tools or None,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": schema_name,
                        "schema": schema,
                        "strict": True,
                    }
                },
            )

        except Exception as exc:
            logger.exception(
                "OpenAI structured request failed."
            )

            raise OpenAIRequestError(
                "OpenAI structured request failed."
            ) from exc

        raw_text = response.output_text

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise OpenAIRequestError(
                "OpenAI returned invalid JSON."
            ) from exc

        return {
            "response_id": response.id,
            "data": parsed,
            "raw": response,
        }