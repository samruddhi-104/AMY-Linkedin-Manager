from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.scheduler.service import (
    scheduler_service,
)


router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"],
)


@router.get("")
async def list_calendar():

    return {
        "success": True,
        "data": (
            scheduler_service.list_scheduled()
        ),
    }


@router.post("/schedule")
async def schedule_post(
    payload: dict,
):

    post_id = str(
        payload.get(
            "post_id",
            "",
        )
    ).strip()

    scheduled_at = str(
        payload.get(
            "scheduled_at",
            "",
        )
    ).strip()

    if not post_id:
        raise HTTPException(
            status_code=400,
            detail="post_id is required.",
        )

    if not scheduled_at:
        raise HTTPException(
            status_code=400,
            detail="scheduled_at is required.",
        )

    try:

        parsed_datetime = (
            datetime.fromisoformat(
                scheduled_at
            )
        )

        result = await scheduler_service.schedule(
            post_id,
            parsed_datetime,
        )

        return {
            "success": True,
            "data": result,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{scheduled_id}/cancel"
)
async def cancel_scheduled_post(
    scheduled_id: str,
):

    success = (
        await scheduler_service.cancel(
            scheduled_id
        )
    )

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Scheduled job not found.",
        )

    return {
        "success": True,
        "data": {
            "id": scheduled_id,
            "status": "CANCELLED",
        },
    }