import time
from uuid import uuid4

from app.providers.linkedin.client import (
    LinkedInProvider,
)
from app.providers.linkedin.schemas import (
    LinkedInAccountInfo,
    LinkedInPublishResult,
    LinkedInStatus,
)


class MockLinkedInProvider(
    LinkedInProvider
):

    def __init__(self) -> None:

        self.connected = True

        self.account_id = (
            "MOCK_CT0NS_ACCOUNT"
        )

        self.display_name = (
            "CTons Solutions"
        )

    async def get_status(
        self,
    ) -> LinkedInStatus:

        return LinkedInStatus(
            connected=self.connected,
            account_id=self.account_id,
            display_name=self.display_name,
            account_type="organization",
        )

    async def get_account(
        self,
    ) -> LinkedInAccountInfo:

        return LinkedInAccountInfo(
            account_id=self.account_id,
            display_name=self.display_name,
            account_type="organization",
            connected=self.connected,
        )

    async def publish_text(
        self,
        *,
        author: str,
        commentary: str,
    ) -> LinkedInPublishResult:

        post_id = (
            f"MOCK_POST_{uuid4().hex[:12]}"
        )

        return LinkedInPublishResult(
            success=True,
            post_id=post_id,
            provider="mock",
            url=(
                "https://www.linkedin.com/"
                "feed/update/"
                f"{post_id}"
            ),
        )

    async def publish_image(
        self,
        *,
        author: str,
        commentary: str,
        image_path: str,
    ) -> LinkedInPublishResult:

        post_id = (
            f"MOCK_IMAGE_POST_"
            f"{uuid4().hex[:12]}"
        )

        return LinkedInPublishResult(
            success=True,
            post_id=post_id,
            provider="mock",
            url=(
                "https://www.linkedin.com/"
                "feed/update/"
                f"{post_id}"
            ),
        )