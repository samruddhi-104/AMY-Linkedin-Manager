from pydantic import BaseModel, Field


class CompetitorObservation(BaseModel):
    competitor: str
    topics: list[str] = Field(
        default_factory=list
    )
    content_formats: list[str] = Field(
        default_factory=list
    )
    hook_patterns: list[str] = Field(
        default_factory=list
    )
    cta_patterns: list[str] = Field(
        default_factory=list
    )
    positioning: list[str] = Field(
        default_factory=list
    )
    opportunities_for_ctons: list[str] = Field(
        default_factory=list
    )


class CompetitorResearchResult(BaseModel):
    summary: str
    observations: list[CompetitorObservation]