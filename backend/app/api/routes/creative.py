import asyncio

from fastapi import APIRouter, HTTPException

from app.agents.creative_agent import CreativeAgent
from app.api.websocket import manager
from app.orchestrator.task_manager import TaskManager
from app.services.in_memory_store import store


router = APIRouter(
    prefix="/creative",
    tags=["Creative"],
)


task_manager = TaskManager()


@router.get("")
async def list_assets():

    return {
        "success": True,
        "data": store.list_assets(),
    }


@router.post("/generate")
async def generate_creative(
    payload: dict,
):

    post_id = str(
        payload.get(
            "post_id",
            "",
        )
    ).strip()

    if not post_id:

        raise HTTPException(
            status_code=400,
            detail="post_id is required.",
        )

    post = store.get_post(
        post_id
    )

    if post is None:

        raise HTTPException(
            status_code=404,
            detail="Post not found.",
        )

    task = task_manager.create_task(
        command=(
            f"Create an image for post {post_id}"
        ),
        task_type="CREATIVE_GENERATION",
    )

    task_id = task["id"]

    async def run_creative():

        try:

            task_manager.update_task(
                task_id,
                status="RUNNING",
                progress=10,
            )

            await manager.broadcast(
                {
                    "type": "task.started",
                    "task_id": task_id,
                    "intent": "CREATIVE_GENERATION",
                }
            )

            agent = CreativeAgent()

            result = await agent.run(
                task_id=task_id,
                input_data={
                    "post_id": post_id,
                },
            )

            task_manager.update_task(
                task_id,
                status="COMPLETED",
                progress=100,
                result=result,
            )

            await manager.broadcast(
                {
                    "type": "task.completed",
                    "task_id": task_id,
                    "result": result,
                }
            )

        except Exception as exc:

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

    asyncio.create_task(
        run_creative()
    )

    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": "QUEUED",
        },
    }