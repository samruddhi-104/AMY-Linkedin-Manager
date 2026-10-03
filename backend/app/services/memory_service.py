from typing import Any
from uuid import uuid4

from app.services.in_memory_store import store


class MemoryService:
    """
    Temporary memory service.

    Phase 3:
        simple keyword/semantic-like matching

    Future:
        PostgreSQL + pgvector embeddings
    """

    def save(
        self,
        content: str,
        memory_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        memory = {
            "id": str(uuid4()),
            "content": content,
            "memory_type": memory_type,
            "metadata": metadata or {},
        }

        store.add_memory(memory)

        return memory

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        query_words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        scored: list[tuple[int, dict[str, Any]]] = []

        for memory in store.list_memory():

            content = memory.get(
                "content",
                "",
            ).lower()

            score = sum(
                1
                for word in query_words
                if word in content
            )

            if score > 0:
                scored.append(
                    (
                        score,
                        memory,
                    )
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            item[1]
            for item in scored[:limit]
        ]

    def delete(
        self,
        memory_id: str,
    ) -> bool:

        return store.delete_memory(
            memory_id
        )

    def list_all(
        self,
    ) -> list[dict[str, Any]]:

        return store.list_memory()


memory_service = MemoryService()