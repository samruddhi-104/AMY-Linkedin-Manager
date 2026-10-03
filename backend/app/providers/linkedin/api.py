import logging

import httpx

from app.config import get_settings
from app.providers.linkedin.client import (
    LinkedInProvider,
)
from app.providers.linkedin.schemas import (
    LinkedInAccountInfo,
    LinkedInPublishResult,
    LinkedInStatus,
)


logger = logging.getLogger(__name__)


class RealLinkedInProvider(
    LinkedInProvider
):

    BASE_URL = (
        "https://api.linkedin.com"
    )

    def __init__(
        self,
        access_token: str,
    ) -> None:

        self.settings = get_settings()

        if not access_token:
            raise ValueError(
                "LinkedIn access token is required."
            )

        self.access_token = access_token

    def _headers(self) -> dict[str, str]:

        version = (
            self.settings.linkedin_api_version
        )

        if not version:
            raise ValueError(
                "LINKEDIN_API_VERSION must be configured."
            )

        return {
            "Authorization": (
                f"Bearer {self.access_token}"
            ),
            "Content-Type": (
                "application/json"
            ),
            "X-Restli-Protocol-Version": (
                "2.0.0"
            ),
            "Linkedin-Version": version,
        }

    async def get_status(
        self,
    ) -> LinkedInStatus:

        try:
            async with httpx.AsyncClient(
                timeout=30
            ) as client:

                response = await client.get(
                    f"{self.BASE_URL}/v2/userinfo",
                    headers=self._headers(),
                )

                response.raise_for_status()

                data = response.json()

                return LinkedInStatus(
                    connected=True,
                    account_id=data.get(
                        "sub",
                        "",
                    ),
                    display_name=data.get(
                        "name",
                    ),
                    account_type="member",
                )

        except Exception:

            logger.exception(
                "LinkedIn status request failed."
            )

            raise

    async def get_account(
        self,
    ) -> LinkedInAccountInfo:

        status = (
            await self.get_status()
        )

        return LinkedInAccountInfo(
            account_id=(
                status.account_id
                or ""
            ),
            display_name=(
                status.display_name
                or "LinkedIn Account"
            ),
            account_type=(
                status.account_type
                or "member"
            ),
            connected=status.connected,
        )

    async def publish_text(
        self,
        *,
        author: str,
        commentary: str,
    ) -> LinkedInPublishResult:

        payload = {
            "author": author,
            "commentary": commentary,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }

        try:

            async with httpx.AsyncClient(
                timeout=60
            ) as client:

                response = await client.post(
                    f"{self.BASE_URL}/rest/posts",
                    headers=self._headers(),
                    json=payload,
                )

                response.raise_for_status()

                linkedin_post_id = (
                    response.headers.get(
                        "x-restli-id"
                    )
                )

                if not linkedin_post_id:

                    response_data = (
                        response.json()
                        if response.content
                        else {}
                    )

                    linkedin_post_id = (
                        response_data.get(
                            "id"
                        )
                    )

                if not linkedin_post_id:

                    raise RuntimeError(
                        "LinkedIn did not return a post ID."
                    )

                return LinkedInPublishResult(
                    success=True,
                    post_id=linkedin_post_id,
                    provider="linkedin",
                    url=None,
                )

        except Exception:

            logger.exception(
                "LinkedIn text publishing failed."
            )

            raise

    async def publish_image(
        self,
        *,
        author: str,
        commentary: str,
        image_path: str,
    ) -> LinkedInPublishResult:

        raise NotImplementedError(
            "Real LinkedIn image publishing "
            "will be added after media-upload "
            "permissions/API handling is configured."
        )