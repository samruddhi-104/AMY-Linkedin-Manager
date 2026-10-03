import asyncio

from fastapi import APIRouter, HTTPException

from app.agents.content_agent import ContentAgent
from app.api.websocket import manager
from app.orchestrator.task_manager import TaskManager
from app.services.in_memory_store import store
from app.services.approval_service import approval_service


router = APIRouter(
    prefix="/content",
    tags=["Content"],
)


task_manager = TaskManager()


@router.get("")
async def list_content():

    return {
        "success": True,
        "data": store.list_posts(),
    }


@router.get("/{post_id}")
async def get_content(
    post_id: str,
):

    post = store.get_post(
        post_id
    )

    if post is None:

        raise HTTPException(
            status_code=404,
            detail="Post not found.",
        )

    return {
        "success": True,
        "data": post,
    }


@router.post("/generate")
async def generate_content(
    payload: dict,
):

    topic = str(
        payload.get(
            "topic",
            "",
        )
    ).strip()

    if not topic:

        raise HTTPException(
            status_code=400,
            detail="Topic is required.",
        )

    task = task_manager.create_task(
        command=f"Create a LinkedIn post about {topic}",
        task_type="CONTENT_GENERATION",
    )

    task_id = task["id"]

    async def run_content():

        try:

            await manager.broadcast(
                {
                    "type": "task.created",
                    "task_id": task_id,
                    "intent": "CONTENT_GENERATION",
                }
            )

            task_manager.update_task(
                task_id,
                status="RUNNING",
                progress=10,
            )

            await manager.broadcast(
                {
                    "type": "task.started",
                    "task_id": task_id,
                    "intent": "CONTENT_GENERATION",
                }
            )

            agent = ContentAgent()

            result = await agent.run(
                task_id=task_id,
                input_data={
                    "topic": topic,
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
        run_content()
    )

    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": "QUEUED",
        },
    }


@router.post("/{post_id}/review")
async def submit_for_review(
    post_id: str,
):

    try:

        post = (
            approval_service.submit_for_review(
                post_id
            )
        )

        return {
            "success": True,
            "data": post,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post("/{post_id}/approve")
async def approve_post(
    post_id: str,
):

    try:

        post = (
            approval_service.approve(
                post_id
            )
        )

        return {
            "success": True,
            "data": post,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )