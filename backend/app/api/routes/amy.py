import asyncio

from fastapi import APIRouter

from app.api.websocket import manager
from app.orchestrator.executor import TaskExecutor
from app.orchestrator.router import CommandRouter
from app.orchestrator.task_manager import TaskManager


router = APIRouter(
    prefix="/amy",
    tags=["AMY"],
)


command_router = CommandRouter()
task_manager = TaskManager()
executor = TaskExecutor()


@router.post("/command")
async def command(
    payload: dict,
):

    message = str(
        payload.get(
            "message",
            "",
        )
    ).strip()

    if not message:

        return {
            "success": False,
            "error": {
                "code": "EMPTY_COMMAND",
                "message": (
                    "Command cannot be empty."
                ),
                "details": {},
            },
        }

    intent = command_router.classify(
        message
    )

    task = task_manager.create_task(
        command=message,
        task_type=intent,
    )

    task_id = task["id"]

    await manager.broadcast(
        {
            "type": "task.created",
            "task_id": task_id,
            "intent": intent,
            "command": message,
        }
    )

    asyncio.create_task(
        executor.execute(
            task_id=task_id,
            command=message,
            task_manager=task_manager,
        )
    )

    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "intent": intent,
            "status": "QUEUED",
            "message": (
                "AMY received your command "
                "and started the task."
            ),
        },
    }