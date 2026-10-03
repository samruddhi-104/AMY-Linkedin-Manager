from uuid import UUID

from pydantic import BaseModel


class AgentResponse(BaseModel):
    id: UUID
    name: str
    display_name: str
    description: str | None
    version: str
    status: str
    enabled: bool
    capabilities: list | None

    model_config = {
        "from_attributes": True,
    }