import logging
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.agents.base_agent import BaseAgent
from app.agents.creative_agent.prompts import SYSTEM_PROMPT
from app.agents.creative_agent.schemas import CreativeResult
from app.config import get_settings
from app.providers.openai.image import (
    OpenAIImageProvider,
)
from app.services.in_memory_store import store


logger = logging.getLogger(__name__)


CREATIVE_SCHEMA = {
    "type": "object",
    "properties": {
        "concept": {
            "type": "string",
        },
        "image_prompt": {
            "type": "string",
        },
        "aspect_ratio": {
            "type": "string",
        },
    },
    "required": [
        "concept",
        "image_prompt",
        "aspect_ratio",
    ],
    "additionalProperties": False,
}


class CreativeAgent(BaseAgent):

    name = "creative"

    display_name = "Creative Agent"

    version = "3.0.0"

    capabilities = [
        "IMAGE_GENERATION",
        "ASSET_WRITE",
    ]

    async def run(
        self,
        task_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        self.status = "RUNNING"

        start = time.perf_counter()

        post_id = str(
            input_data.get(
                "post_id",
                "",
            )
        ).strip()

        if not post_id:

            self.status = "FAILED"

            raise ValueError(
                "post_id is required."
            )

        post = store.get_post(
            post_id
        )

        if post is None:

            self.status = "FAILED"

            raise ValueError(
                "Post not found."
            )

        try:

            settings = get_settings()

            # -------------------------------------------------
            # Generate visual concept
            # -------------------------------------------------

            post_text = (
                f"Title: {post.get('title', '')}\n"
                f"Hook: {post.get('hook', '')}\n"
                f"Body: {post.get('body', '')}\n"
                f"CTA: {post.get('cta', '')}\n"
            )

            if settings.mock_mode:

                concept = (
                    "A premium B2B technology visual "
                    "showing an AI agent coordinating "
                    "multiple business systems."
                )

                image_prompt = (
                    "Create a premium professional "
                    "LinkedIn technology visual about "
                    "AI agents coordinating multiple "
                    "business workflows. Modern B2B "
                    "aesthetic, clean dark background, "
                    "subtle luminous interface elements, "
                    "strong visual hierarchy, no clutter, "
                    "no unnecessary text."
                )

                # Create a simple SVG mock asset.

                asset_id = str(
                    uuid4()
                )

                output_dir = (
                    settings.storage_path
                    / "generated"
                    / "images"
                )

                output_dir.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                output_path = (
                    output_dir
                    / f"{asset_id}.svg"
                )

                svg = f"""
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="1024"
    height="1024"
    viewBox="0 0 1024 1024"
>
    <rect
        width="1024"
        height="1024"
        fill="#0b1020"
    />

    <circle
        cx="512"
        cy="400"
        r="150"
        fill="none"
        stroke="#5eead4"
        stroke-width="5"
    />

    <circle
        cx="512"
        cy="400"
        r="95"
        fill="none"
        stroke="#60a5fa"
        stroke-width="4"
    />

    <text
        x="512"
        y="410"
        text-anchor="middle"
        fill="#ffffff"
        font-family="Arial, sans-serif"
        font-size="42"
        font-weight="bold"
    >
        AI AGENTS
    </text>

    <line
        x1="360"
        y1="560"
        x2="230"
        y2="700"
        stroke="#60a5fa"
        stroke-width="5"
    />

    <line
        x1="664"
        y1="560"
        x2="794"
        y2="700"
        stroke="#60a5fa"
        stroke-width="5"
    />

    <rect
        x="120"
        y="700"
        width="220"
        height="90"
        rx="20"
        fill="#111827"
        stroke="#60a5fa"
        stroke-width="3"
    />

    <text
        x="230"
        y="755"
        text-anchor="middle"
        fill="#ffffff"
        font-family="Arial, sans-serif"
        font-size="24"
    >
        BUSINESS
    </text>

    <rect
        x="684"
        y="700"
        width="220"
        height="90"
        rx="20"
        fill="#111827"
        stroke="#60a5fa"
        stroke-width="3"
    />

    <text
        x="794"
        y="755"
        text-anchor="middle"
        fill="#ffffff"
        font-family="Arial, sans-serif"
        font-size="24"
    >
        AUTOMATION
    </text>
</svg>
"""

                output_path.write_text(
                    svg,
                    encoding="utf-8",
                )

                asset = {
                    "id": asset_id,
                    "post_id": post_id,
                    "asset_type": "image",
                    "file_path": str(
                        output_path
                    ),
                    "mime_type": "image/svg+xml",
                    "provider": "mock",
                    "created_at": time.time(),
                }

            else:

                from app.providers.openai.client import (
                    OpenAIProvider,
                )

                openai = OpenAIProvider()

                prompt = f"""
Create a professional LinkedIn visual concept.

POST:
{post_text}

CTONS VISUAL STYLE:
Modern
Professional
Premium B2B technology
Clean composition
Strong hierarchy

Do not create a generic stock photo.

Return:

concept
image_prompt
aspect_ratio
"""

                response = (
                    await openai.generate_json(
                        instructions=SYSTEM_PROMPT,
                        input_text=prompt,
                        schema_name="creative_concept",
                        schema=CREATIVE_SCHEMA,
                        use_web_search=False,
                    )
                )

                concept_data = response[
                    "data"
                ]

                concept = concept_data[
                    "concept"
                ]

                image_prompt = concept_data[
                    "image_prompt"
                ]

                asset_id = str(
                    uuid4()
                )

                output_dir = (
                    settings.storage_path
                    / "generated"
                    / "images"
                )

                output_path = (
                    output_dir
                    / f"{asset_id}.png"
                )

                image_provider = (
                    OpenAIImageProvider()
                )

                generated = (
                    await image_provider.generate(
                        prompt=image_prompt,
                        output_path=output_path,
                    )
                )

                asset = {
                    "id": asset_id,
                    "post_id": post_id,
                    "asset_type": "image",
                    "file_path": generated[
                        "file_path"
                    ],
                    "mime_type": "image/png",
                    "provider": "openai",
                    "created_at": time.time(),
                }

            # -------------------------------------------------
            # Save asset
            # -------------------------------------------------

            store.add_asset(
                asset
            )

            duration_ms = int(
                (
                    time.perf_counter()
                    - start
                )
                * 1000
            )

            self.status = "COMPLETED"

            result = CreativeResult(
                post_id=post_id,
                concept=concept,
                image_prompt=image_prompt,
                aspect_ratio="1:1",
                asset_id=asset["id"],
                asset_path=asset[
                    "file_path"
                ],
            )

            return {
                "agent": self.name,
                "task_id": task_id,
                "status": "COMPLETED",
                "duration_ms": duration_ms,
                "result": result.model_dump(),
            }

        except Exception:

            self.status = "FAILED"

            logger.exception(
                "Creative agent failed."
            )

            raise