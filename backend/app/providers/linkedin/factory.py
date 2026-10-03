from app.config import get_settings
from app.providers.linkedin.mock_linkedin import (
    MockLinkedInProvider,
)
from app.providers.linkedin.api import (
    RealLinkedInProvider,
)


def get_linkedin_provider():

    settings = get_settings()

    if settings.mock_mode:

        return MockLinkedInProvider()

    account_token = (
        getattr(
            settings,
            "linkedin_access_token",
            None,
        )
    )

    if not account_token:

        raise RuntimeError(
            "LinkedIn is not connected."
        )

    return RealLinkedInProvider(
        access_token=account_token
    )