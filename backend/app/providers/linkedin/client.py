from abc import ABC, abstractmethod

from app.providers.linkedin.schemas import (
    LinkedInAccountInfo,
    LinkedInPublishResult,
    LinkedInStatus,
)


class LinkedInProvider(ABC):

    @abstractmethod
    async def get_status(
        self,
    ) -> LinkedInStatus:
        raise NotImplementedError

    @abstractmethod
    async def get_account(
        self,
    ) -> LinkedInAccountInfo:
        raise NotImplementedError

    @abstractmethod
    async def publish_text(
        self,
        *,
        author: str,
        commentary: str,
    ) -> LinkedInPublishResult:
        raise NotImplementedError

    @abstractmethod
    async def publish_image(
        self,
        *,
        author: str,
        commentary: str,
        image_path: str,
    ) -> LinkedInPublishResult:
        raise NotImplementedError