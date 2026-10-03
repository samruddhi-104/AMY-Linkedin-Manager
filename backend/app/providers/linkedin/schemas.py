from pydantic import BaseModel


class LinkedInAccountInfo(BaseModel):
    provider: str = "linkedin"

    account_id: str

    display_name: str

    account_type: str

    connected: bool = True


class LinkedInPublishResult(BaseModel):

    success: bool

    post_id: str

    provider: str

    url: str | None = None


class LinkedInStatus(BaseModel):

    connected: bool

    account_id: str | None = None

    display_name: str | None = None

    account_type: str | None = None