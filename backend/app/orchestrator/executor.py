import asyncio
import logging
from typing import Any

from app.agents.base_agent import BaseAgent
from app.api.websocket import manager
from app.orchestrator.agent_manager import AgentManager
from app.orchestrator.router import CommandRouter
from app.orchestrator.task_manager import TaskManager
from app.scheduler.service import scheduler_service


logger = logging.getLogger(__name__)


class TaskExecutor:

    def __init__(self) -> None:

        self.router = CommandRouter()

        self.agent_manager = (
            AgentManager()
        )

    def _build_plan(
        self,
        intent: str,
    ) -> list[str]:

        plans = {
            "RESEARCH": [
                "research",
            ],

            "COMPETITOR_RESEARCH": [
                "competitor",
            ],

            "KEYWORD_RESEARCH": [
                "keyword",
            ],

            "CONTENT_GENERATION": [
                "content",
            ],

            "CREATIVE_GENERATION": [
                "creative",
            ],

            "LINKEDIN_PUBLISH": [
                "linkedin",
            ],

            "LINKEDIN_SCHEDULE": [],
        }

        return plans.get(
            intent,
            [],
        )

    async def _run_agent(
        self,
        *,
        task_id: str,
        agent_name: str,
        command: str,
        task_manager: TaskManager,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        agent = (
            self.agent_manager.create_agent(
                agent_name
            )
        )

        self.agent_manager.register_active(
            task_id,
            agent,
        )

        await manager.broadcast(
            {
                "type": "agent.started",
                "task_id": task_id,
                "agent": agent_name,
            }
        )

        await manager.broadcast(
            {
                "type": "agent.progress",
                "task_id": task_id,
                "agent": agent_name,
                "progress": 15,
                "message": (
                    f"{agent.display_name} "
                    "started working."
                ),
            }
        )

        try:

            result = await agent.run(
                task_id=task_id,
                input_data=input_data,
            )

            await manager.broadcast(
                {
                    "type": "agent.progress",
                    "task_id": task_id,
                    "agent": agent_name,
                    "progress": 90,
                    "message": (
                        f"{agent.display_name} "
                        "completed processing."
                    ),
                }
            )

            await manager.broadcast(
                {
                    "type": "agent.completed",
                    "task_id": task_id,
                    "agent": agent_name,
                    "progress": 100,
                }
            )

            return result

        finally:

            await self.agent_manager.remove_active(
                task_id
            )

    async def execute(
        self,
        task_id: str,
        command: str,
        task_manager: TaskManager,
    ) -> None:

        intent = self.router.classify(
            command
        )

        # ---------------------------------------------
        # LinkedIn Schedule
        # ---------------------------------------------

        if intent == "LINKEDIN_SCHEDULE":

            from datetime import datetime

            raise ValueError(
                "Scheduling through natural language "
                "will be completed with the voice/"
                "planner layer. Use the calendar API "
                "for Phase 4 testing."
            )

        plan = self._build_plan(
            intent
        )

        if not plan:

            task_manager.update_task(
                task_id,
                status="COMPLETED",
                progress=100,
                result={
                    "intent": intent,
                    "message": (
                        "AMY understood the command, "
                        "but the requested capability "
                        "is not implemented yet."
                    ),
                },
            )

            await manager.broadcast(
                {
                    "type": "task.completed",
                    "task_id": task_id,
                    "intent": intent,
                }
            )

            return

        task_manager.update_task(
            task_id,
            status="RUNNING",
            progress=5,
        )

        await manager.broadcast(
            {
                "type": "task.started",
                "task_id": task_id,
                "intent": intent,
            }
        )

        final_results: dict[
            str,
            Any,
        ] = {}

        try:

            for index, agent_name in enumerate(
                plan
            ):

                progress = min(
                    90,
                    10 + index * 25,
                )

                task_manager.update_task(
                    task_id,
                    progress=progress,
                )

                # ---------------------------------------------
                # Input preparation
                # ---------------------------------------------

                input_data: dict[
                    str,
                    Any,
                ] = {
                    "topic": command,
                }

                if intent == "COMPETITOR_RESEARCH":

                    input_data[
                        "competitors"
                    ] = [
                        "AI automation companies",
                        "enterprise AI companies",
                    ]

                # ---------------------------------------------
                # Creative command
                # ---------------------------------------------

                if intent == "CREATIVE_GENERATION":

                    from app.services.in_memory_store import (
                        store,
                    )

                    posts = store.list_posts()

                    if not posts:
                        raise ValueError(
                            "There is no post available "
                            "for image generation."
                        )

                    input_data = {
                        "post_id": posts[-1]["id"],
                    }

                # ---------------------------------------------
                # Content command
                # ---------------------------------------------

                if intent == "CONTENT_GENERATION":

                    input_data = {
                        "topic": command,
                    }

                # ---------------------------------------------
                # LinkedIn publishing command
                # ---------------------------------------------

                if intent == "LINKEDIN_PUBLISH":

                    input_data = {
                        "topic": command,
                    }

                result = await self._run_agent(
                    task_id=task_id,
                    agent_name=agent_name,
                    command=command,
                    task_manager=task_manager,
                    input_data=input_data,
                )

                final_results[
                    agent_name
                ] = result

            task_manager.update_task(
                task_id,
                status="COMPLETED",
                progress=100,
                result={
                    "intent": intent,
                    "agents": final_results,
                },
            )

            await manager.broadcast(
                {
                    "type": "task.completed",
                    "task_id": task_id,
                    "progress": 100,
                    "result": final_results,
                }
            )

        except asyncio.CancelledError:

            task_manager.update_task(
                task_id,
                status="CANCELLED",
            )

            await manager.broadcast(
                {
                    "type": "task.cancelled",
                    "task_id": task_id,
                }
            )

            raise

        except Exception as exc:

            logger.exception(
                "Task execution failed."
            )

            task_manager.update_task(
                task_id,
                status="FAILED",
                error=str(exc),
            )

            await manager.broadcast(
                {
                    "type": "task.failed",
                    "task_id": task_id,
                    "error": str(exc),
                }
            )

