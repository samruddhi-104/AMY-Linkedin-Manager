from fastapi import APIRouter

from app.services.memory_service import memory_service
from app.services.in_memory_store import store


router = APIRouter(
    prefix="/memory",
    tags=["Memory"],
)


@router.get("")
async def list_memory():

    return {
        "success": True,
        "data": memory_service.list_all(),
    }


@router.get("/search")
async def search_memory(
    q: str,
):

    return {
        "success": True,
        "data": memory_service.search(
            q
        ),
    }


@router.get("/company")
async def company_profile():

    return {
        "success": True,
        "data": store.get_company_profile(),
    }