from abc import ABC, abstractmethod
from typing import Any


class SearchProvider(ABC):

    @abstractmethod
    async def search(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def fetch(
        self,
        url: str,
    ) -> dict[str, Any]:
        raise NotImplementedError