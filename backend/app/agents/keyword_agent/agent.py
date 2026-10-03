import logging
import time
from typing import Any

from app.agents.base_agent import BaseAgent
from app.agents.keyword_agent.prompts import SYSTEM_PROMPT
from app.agents.keyword_agent.schemas import (
    Hashtag,
    Keyword,
    KeywordResearchResult,
)
from app.config import get_settings
from app.providers.factory import (
    get_openai_provider,
    get_search_provider,
)


logger = logging.getLogger(__name__)


KEYWORD_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {
            "type": "string",
        },
        "primary_keywords": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    },
                    "keyword_type": {
                        "type": "string",
                    },
                    "relevance_score": {
                        "type": "number",
                    },
                    "reason": {
                        "type": "string",
                    },
                },
                "required": [
                    "keyword",
                    "keyword_type",
                    "relevance_score",
                    "reason",
                ],
                "additionalProperties": False,
            },
        },
        "secondary_keywords": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    },
                    "keyword_type": {
                        "type": "string",
                    },
                    "relevance_score": {
                        "type": "number",
                    },
                    "reason": {
                        "type": "string",
                    },
                },
                "required": [
                    "keyword",
                    "keyword_type",
                    "relevance_score",
                    "reason",
                ],
                "additionalProperties": False,
            },
        },
        "long_tail_keywords": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    },
                    "keyword_type": {
                        "type": "string",
                    },
                    "relevance_score": {
                        "type": "number",
                    },
                    "reason": {
                        "type": "string",
                    },
                },
                "required": [
                    "keyword",
                    "keyword_type",
                    "relevance_score",
                    "reason",
                ],
                "additionalProperties": False,
            },
        },
        "hashtags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "hashtag": {
                        "type": "string",
                    },
                    "relevance_score": {
                        "type": "number",
                    },
                    "reason": {
                        "type": "string",
                    },
                },
                "required": [
                    "hashtag",
                    "relevance_score",
                    "reason",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "topic",
        "primary_keywords",
        "secondary_keywords",
        "long_tail_keywords",
        "hashtags",
    ],
    "additionalProperties": False,
}


class KeywordAgent(BaseAgent):

    name = "keyword"
    display_name = "Keyword Agent"
    version = "2.0.0"

    capabilities = [
        "WEB_SEARCH",
        "KEYWORD_RESEARCH",
        "HASHTAG_RESEARCH",
    ]

    async def run(
        self,
        task_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        self.status = "RUNNING"

        topic = str(
            input_data.get(
                "topic",
                "",
            )
        ).strip()

        if not topic:
            self.status = "FAILED"

            raise ValueError(
                "Keyword research topic is required."
            )

        start = time.perf_counter()

        try:

            search_provider = get_search_provider()

            search_context = (
                await search_provider.search(
                    f"keywords hashtags {topic}"
                )
            )

            settings = get_settings()

            if settings.mock_mode:

                result = KeywordResearchResult(
                    topic=topic,
                    primary_keywords=[
                        Keyword(
                            keyword=topic,
                            keyword_type="primary",
                            relevance_score=1.0,
                            reason=(
                                "Direct match to "
                                "the requested topic."
                            ),
                        ),
                        Keyword(
                            keyword="AI agents",
                            keyword_type="primary",
                            relevance_score=0.95,
                            reason=(
                                "Core concept for "
                                "the topic."
                            ),
                        ),
                    ],
                    secondary_keywords=[
                        Keyword(
                            keyword="business automation",
                            keyword_type="secondary",
                            relevance_score=0.9,
                            reason=(
                                "Relevant business "
                                "application."
                            ),
                        ),
                        Keyword(
                            keyword="enterprise AI",
                            keyword_type="secondary",
                            relevance_score=0.85,
                            reason=(
                                "Strong enterprise "
                                "context."
                            ),
                        ),
                    ],
                    long_tail_keywords=[
                        Keyword(
                            keyword=(
                                "AI agents for business "
                                "automation"
                            ),
                            keyword_type="long_tail",
                            relevance_score=0.9,
                            reason=(
                                "Specific business "
                                "search intent."
                            ),
                        ),
                    ],
                    hashtags=[
                        Hashtag(
                            hashtag="#AIAgents",
                            relevance_score=0.95,
                            reason=(
                                "Directly relevant "
                                "to the topic."
                            ),
                        ),
                        Hashtag(
                            hashtag="#AI",
                            relevance_score=0.9,
                            reason=(
                                "Broad industry "
                                "relevance."
                            ),
                        ),
                        Hashtag(
                            hashtag="#Automation",
                            relevance_score=0.9,
                            reason=(
                                "Relevant to "
                                "business automation."
                            ),
                        ),
                    ],
                )

            else:

                openai = get_openai_provider()

                prompt = f"""
Research useful keywords and hashtags for:

{topic}

Additional research material:

{search_context}
"""

                response = await openai.generate_json(
                    instructions=SYSTEM_PROMPT,
                    input_text=prompt,
                    schema_name="keyword_research_result",
                    schema=KEYWORD_SCHEMA,
                    use_web_search=True,
                )

                result = (
                    KeywordResearchResult.model_validate(
                        response["data"]
                    )
                )

            duration_ms = int(
                (time.perf_counter() - start) * 1000
            )

            self.status = "COMPLETED"

            return {
                "agent": self.name,
                "task_id": task_id,
                "status": "COMPLETED",
                "duration_ms": duration_ms,
                "result": result.model_dump(),
            }

        except Exception:

            self.status = "FAILED"

            logger.exception(
                "Keyword agent failed."
            )

            raise