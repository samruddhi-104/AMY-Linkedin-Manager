from pydantic import BaseModel, Field


class ResearchSource(BaseModel):

    title: str

    url: str

    domain: str

    published_at: str | None = None

    source_type: str

    summary: str


class ResearchResult(BaseModel):

    topic: str

    summary: str

    trends: list[str] = Field(
        default_factory=list
    )

    important_findings: list[str] = Field(
        default_factory=list
    )

    content_opportunities: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )

    sources: list[ResearchSource] = Field(
        default_factory=list
    )