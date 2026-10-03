from typing import Any

from app.services.in_memory_store import store
from app.tasks.task_states import TaskStatus


class TaskManager:

    def create_task(
        self,
        command: str,
        task_type: str = "GENERAL",
        priority: str = "normal",
    ) -> dict[str, Any]:

        return store.create_task(
            command=command,
            task_type=task_type,
            priority=priority,
        )

    def get_task(
        self,
        task_id: str,
    ) -> dict[str, Any] | None:

        return store.get_task(task_id)

    def list_tasks(self) -> list[dict[str, Any]]:
        return store.list_tasks()

    def update_task(
        self,
        task_id: str,
        **updates: Any,
    ) -> dict[str, Any] | None:

        return store.update_task(
            task_id,
            **updates,
        )

    def cancel_task(
        self,
        task_id: str,
    ) -> dict[str, Any] | None:

        return store.update_task(
            task_id,
            status=TaskStatus.CANCEL_REQUESTED.value,
        )