from dataclasses import dataclass
from typing import Any


@dataclass
class ExecutionContext:
    task_id: str
    command: str
    company_id: str | None = None
    metadata: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "command": self.command,
            "company_id": self.company_id,
            "metadata": self.metadata or {},
        }