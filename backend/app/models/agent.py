import logging
import time
from typing import Any

from app.agents.base_agent import BaseAgent
from app.config import get_settings
from app.providers.linkedin.factory import (
    get_linkedin_provider,
)
from app.services.in_memory_store import store


logger = logging.getLogger(__name__)


class LinkedInAgent(BaseAgent):

    name = "linkedin"

    display_name = "LinkedIn Agent"

    version = "4.0.0"

    capabilities = [
        "LINKEDIN_READ",
        "LINKEDIN_PUBLISH",
    ]

    async def run(
        self,
        task_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        self.status = "RUNNING"

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

        post = store.get_post(post_id)

        if post is None:
            self.status = "FAILED"
            raise ValueError(
                "Post not found."
            )

        if post.get("status") != "APPROVED":
            self.status = "FAILED"
            raise ValueError(
                "Only APPROVED posts can be published."
            )

        if post.get("linkedin_post_id"):

            self.status = "COMPLETED"

            return {
                "agent": self.name,
                "task_id": task_id,
                "status": "ALREADY_PUBLISHED",
                "post_id": post_id,
                "linkedin_post_id": (
                    post["linkedin_post_id"]
                ),
            }

        start = time.perf_counter()

        try:

            provider = get_linkedin_provider()

            linkedin_status = (
                await provider.get_status()
            )

            if not linkedin_status.connected:
                raise RuntimeError(
                    "LinkedIn account is not connected."
                )

            settings = get_settings()

            author = (
                settings.linkedin_author_urn
            )

            if not author:

                if settings.mock_mode:
                    author = (
                        "urn:li:organization:MOCK_CT0NS"
                    )
                else:
                    raise RuntimeError(
                        "LINKEDIN_AUTHOR_URN "
                        "is not configured."
                    )

            commentary = (
                f"{post.get('hook', '')}\n\n"
                f"{post.get('body', '')}\n\n"
                f"{post.get('cta', '')}\n\n"
                f"{' '.join(post.get('hashtags', []))}"
            ).strip()

            result = await provider.publish_text(
                author=author,
                commentary=commentary,
            )

            post["linkedin_post_id"] = (
                result.post_id
            )

            post["status"] = "PUBLISHED"

            duration_ms = int(
                (
                    time.perf_counter()
                    - start
                ) * 1000
            )

            store.add_publish_attempt(
                {
                    "task_id": task_id,
                    "post_id": post_id,
                    "linkedin_post_id": (
                        result.post_id
                    ),
                    "status": "SUCCESS",
                    "provider": result.provider,
                    "created_at": time.time(),
                }
            )

            self.status = "COMPLETED"

            return {
                "agent": self.name,
                "task_id": task_id,
                "status": "PUBLISHED",
                "post_id": post_id,
                "linkedin_post_id": (
                    result.post_id
                ),
                "provider": result.provider,
                "duration_ms": duration_ms,
            }

        except Exception as exc:

            self.status = "FAILED"

            store.add_publish_attempt(
                {
                    "task_id": task_id,
                    "post_id": post_id,
                    "status": "FAILED",
                    "error": str(exc),
                    "created_at": time.time(),
                }
            )

            logger.exception(
                "LinkedIn publication failed."
            )

            raise