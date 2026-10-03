from fastapi import APIRouter, HTTPException

from app.orchestrator.task_manager import TaskManager
from app.schemas.task import TaskCreate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


task_manager = TaskManager()


@router.post("")
async def create_task(
    payload: TaskCreate,
):
    task = task_manager.create_task(
        command=payload.command,
        task_type=payload.task_type,
        priority=payload.priority,
    )

    return {
        "success": True,
        "data": task,
    }


@router.get("")
async def list_tasks():

    return {
        "success": True,
        "data": task_manager.list_tasks(),
    }


@router.get("/{task_id}")
async def get_task(
    task_id: str,
):

    task = task_manager.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return {
        "success": True,
        "data": task,
    }


@router.post("/{task_id}/cancel")
async def cancel_task(
    task_id: str,
):

    task = task_manager.cancel_task(
        task_id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return {
        "success": True,
        "data": task,
    }