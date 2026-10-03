from abc import ABC, abstractmethod
from typing import Any

from app.tasks.task_states import AgentStatus


class BaseAgent(ABC):
    name: str = "base"

    display_name: str = "Base Agent"

    version: str = "1.0.0"

    capabilities: list[str] = []

    def __init__(self) -> None:
        self.status = AgentStatus.IDLE.value

    @abstractmethod
    async def run(
        self,
        task_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute the agent task.
        """
        raise NotImplementedError

    async def cancel(self) -> None:
        self.status = AgentStatus.STOPPING.value

    async def health(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "capabilities": self.capabilities,
        }