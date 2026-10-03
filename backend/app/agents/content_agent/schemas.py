from pydantic import BaseModel, Field


class ContentResult(BaseModel):

    content_type: str

    title: str

    hook: str

    body: str

    cta: str

    keywords: list[str] = Field(
        default_factory=list
    )

    hashtags: list[str] = Field(
        default_factory=list
    )

    visual_concept: str

    sources_used: list[str] = Field(
        default_factory=list
    )