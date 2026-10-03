from fastapi import APIRouter

from app.schemas.agent import AgentResponse
from app.services.in_memory_store import store


router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.get("")
async def list_agents():
    return {
        "success": True,
        "data": store.list_agents(),
    }