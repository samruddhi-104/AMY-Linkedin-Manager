from pydantic import BaseModel, Field


class Keyword(BaseModel):
    keyword: str
    keyword_type: str
    relevance_score: float = 0.0
    reason: str


class Hashtag(BaseModel):
    hashtag: str
    relevance_score: float = 0.0
    reason: str


class KeywordResearchResult(BaseModel):
    topic: str

    primary_keywords: list[Keyword] = Field(
        default_factory=list
    )

    secondary_keywords: list[Keyword] = Field(
        default_factory=list
    )

    long_tail_keywords: list[Keyword] = Field(
        default_factory=list
    )

    hashtags: list[Hashtag] = Field(
        default_factory=list
    )