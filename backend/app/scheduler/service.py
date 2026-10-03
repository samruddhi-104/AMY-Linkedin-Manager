import asyncio
import time
from datetime import datetime, timezone
from uuid import uuid4

from app.agents.linkedin_agent import (
    LinkedInAgent,
)
from app.services.in_memory_store import store
from app.tasks.task_states import TaskStatus


class SchedulerService:

    def __init__(self) -> None:

        self.jobs: dict[
            str,
            asyncio.Task,
        ] = {}

    async def schedule(
        self,
        post_id: str,
        scheduled_at: datetime,
    ) -> dict:

        post = store.get_post(
            post_id
        )

        if post is None:
            raise ValueError(
                "Post not found."
            )

        if post.get("status") != "APPROVED":

            raise ValueError(
                "Only approved posts can be scheduled."
            )

        if (
            post.get(
                "linkedin_post_id"
            )
        ):
            raise ValueError(
                "Post has already been published."
            )

        if scheduled_at.tzinfo is None:

            scheduled_at = (
                scheduled_at.replace(
                    tzinfo=timezone.utc
                )
            )

        scheduled_id = str(
            uuid4()
        )

        scheduled_post = {
            "id": scheduled_id,
            "post_id": post_id,
            "scheduled_at": scheduled_at.isoformat(),
            "status": "SCHEDULED",
            "created_at": time.time(),
        }

        store.add_scheduled_post(
            scheduled_post
        )

        post["status"] = "SCHEDULED"

        job = asyncio.create_task(
            self._wait_and_publish(
                scheduled_id,
                post_id,
                scheduled_at,
            )
        )

        self.jobs[
            scheduled_id
        ] = job

        return scheduled_post

    async def _wait_and_publish(
        self,
        scheduled_id: str,
        post_id: str,
        scheduled_at: datetime,
    ) -> None:

        delay = (
            scheduled_at
            - datetime.now(
                timezone.utc
            )
        ).total_seconds()

        if delay > 0:
            await asyncio.sleep(
                delay
            )

        post = store.get_post(
            post_id
        )

        if post is None:
            return

        if post.get("linkedin_post_id"):
            return

        try:

            task_id = str(
                uuid4()
            )

            agent = LinkedInAgent()

            result = await agent.run(
                task_id=task_id,
                input_data={
                    "post_id": post_id,
                },
            )

            store.update_scheduled_post(
                scheduled_id,
                status="PUBLISHED",
                result=result,
            )

        except Exception as exc:

            store.update_scheduled_post(
                scheduled_id,
                status="FAILED",
                error=str(exc),
            )

            post["status"] = "FAILED"

        finally:

            self.jobs.pop(
                scheduled_id,
                None,
            )

    def list_scheduled(self):
        return store.list_scheduled_posts()

    async def cancel(
        self,
        scheduled_id: str,
    ) -> bool:

        job = self.jobs.get(
            scheduled_id
        )

        if job is None:
            return False

        job.cancel()

        store.update_scheduled_post(
            scheduled_id,
            status="CANCELLED",
        )

        return True


scheduler_service = SchedulerService()