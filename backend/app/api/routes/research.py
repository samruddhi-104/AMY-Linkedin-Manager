from fastapi import APIRouter, HTTPException

from app.services.in_memory_store import store


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.get("")
async def list_research():
    """
    Return all research reports stored during
    the current application session.
    """

    return {
        "success": True,
        "data": store.list_research(),
    }


@router.get("/{research_id}")
async def get_research(
    research_id: str,
):
    """
    Return one research report by ID.
    """

    research = store.get_research(
        research_id
    )

    if research is None:
        raise HTTPException(
            status_code=404,
            detail="Research report not found.",
        )

    return {
        "success": True,
        "data": research,
    }