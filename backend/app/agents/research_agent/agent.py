import logging
import time
from typing import Any

from app.agents.base_agent import BaseAgent
from app.agents.research_agent.prompts import SYSTEM_PROMPT
from app.agents.research_agent.schemas import (
    ResearchResult,
)
from app.config import get_settings
from app.providers.factory import (
    get_openai_provider,
    get_search_provider,
)
from app.services.in_memory_store import store


logger = logging.getLogger(__name__)


# =============================================================
# JSON schema used by OpenAI structured output
# =============================================================

RESEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {
            "type": "string",
        },
        "summary": {
            "type": "string",
        },
        "trends": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "important_findings": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "content_opportunities": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                    },
                    "url": {
                        "type": "string",
                    },
                    "domain": {
                        "type": "string",
                    },
                    "published_at": {
                        "type": [
                            "string",
                            "null",
                        ],
                    },
                    "source_type": {
                        "type": "string",
                    },
                    "summary": {
                        "type": "string",
                    },
                },
                "required": [
                    "title",
                    "url",
                    "domain",
                    "published_at",
                    "source_type",
                    "summary",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "topic",
        "summary",
        "trends",
        "important_findings",
        "content_opportunities",
        "recommendations",
        "sources",
    ],
    "additionalProperties": False,
}


class ResearchAgent(BaseAgent):
    """
    CTons AMY Research Agent.

    Responsibilities:

    - research topics
    - analyze recent information
    - identify trends
    - identify important findings
    - identify content opportunities
    - provide recommendations
    - retain source information
    """

    name = "research"

    display_name = "Research Agent"

    version = "2.0.0"

    capabilities = [
        "WEB_SEARCH",
        "WEB_FETCH",
        "RESEARCH",
    ]

    async def run(
        self,
        task_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        self.status = "RUNNING"

        # -----------------------------------------------------
        # Extract topic
        # -----------------------------------------------------

        topic = str(
            input_data.get(
                "topic",
                "",
            )
        ).strip()

        if not topic:

            self.status = "FAILED"

            raise ValueError(
                "Research topic is required."
            )

        start_time = time.perf_counter()

        settings = get_settings()

        try:

            # -------------------------------------------------
            # Get configured search provider
            # -------------------------------------------------

            search_provider = get_search_provider()

            search_results = await search_provider.search(
                topic
            )

            # -------------------------------------------------
            # Convert search results into context
            # -------------------------------------------------

            source_context = "\n\n".join(
                str(result)
                for result in search_results
            )

            research_prompt = f"""
Research the following topic for CTons Solutions:

TOPIC:
{topic}

AVAILABLE RESEARCH MATERIAL:
{source_context}

Your goal is to produce a high-quality research report.

Focus on:

1. Current developments
2. Important trends
3. Important findings
4. Business implications
5. LinkedIn content opportunities
6. Recommended CTons angles
7. Reliable sources

Clearly distinguish facts from interpretation.

Do not fabricate:
- statistics
- URLs
- publication dates
- organizations
- engagement numbers
"""

            # =================================================
            # MOCK MODE
            # =================================================

            if settings.mock_mode:

                result = ResearchResult(
                    topic=topic,

                    summary=(
                        f"Mock research completed for "
                        f"{topic}."
                    ),

                    trends=[
                        (
                            "AI agents are becoming an "
                            "important enterprise topic."
                        ),
                        (
                            "Businesses are exploring "
                            "automation workflows."
                        ),
                    ],

                    important_findings=[
                        (
                            "Organizations are investigating "
                            "AI-based workflow automation."
                        ),
                        (
                            "AI agents are increasingly "
                            "being discussed as productivity "
                            "and automation tools."
                        ),
                    ],

                    content_opportunities=[
                        (
                            "Explain practical AI-agent "
                            "use cases for businesses."
                        ),
                        (
                            "Compare traditional automation "
                            "with AI-agent workflows."
                        ),
                        (
                            "Explain how businesses can "
                            "start adopting AI agents."
                        ),
                    ],

                    recommendations=[
                        (
                            "Use an educational "
                            "thought-leadership approach."
                        ),
                        (
                            "Focus on practical business "
                            "examples instead of generic AI hype."
                        ),
                    ],

                    sources=[
                        {
                            "title": item.get(
                                "title",
                                "Mock Source",
                            ),
                            "url": item.get(
                                "url",
                                "https://example.com",
                            ),
                            "domain": item.get(
                                "domain",
                                "example.com",
                            ),
                            "published_at": item.get(
                                "published_at"
                            ),
                            "source_type": "mock",
                            "summary": item.get(
                                "snippet",
                                "",
                            ),
                        }
                        for item in search_results
                    ],
                )

            # =================================================
            # REAL OPENAI MODE
            # =================================================

            else:

                openai = get_openai_provider()

                response = await openai.generate_json(
                    instructions=SYSTEM_PROMPT,
                    input_text=research_prompt,
                    schema_name="research_result",
                    schema=RESEARCH_SCHEMA,
                    use_web_search=True,
                )

                result = ResearchResult.model_validate(
                    response["data"]
                )

            # -------------------------------------------------
            # Calculate duration
            # -------------------------------------------------

            duration_ms = int(
                (
                    time.perf_counter()
                    - start_time
                )
                * 1000
            )

            # -------------------------------------------------
            # Save research into temporary memory store
            # -------------------------------------------------

            research_id = str(
                time.time_ns()
            )

            stored_research = {
                "id": research_id,
                "task_id": task_id,
                "topic": topic,
                "result": result.model_dump(),
                "created_at": time.time(),
                "duration_ms": duration_ms,
            }

            store.add_research(
                stored_research
            )

            # -------------------------------------------------
            # Mark agent complete
            # -------------------------------------------------

            self.status = "COMPLETED"

            return {
                "agent": self.name,

                "task_id": task_id,

                "status": "COMPLETED",

                "duration_ms": duration_ms,

                "research_id": research_id,

                "result": result.model_dump(),
            }

        except Exception:

            self.status = "FAILED"

            logger.exception(
                "Research agent failed for task %s",
                task_id,
            )

            raise

        finally:

            # -------------------------------------------------
            # Make sure a finished agent does not stay active
            # -------------------------------------------------

            if self.status not in {
                "RUNNING",
                "STOPPING",
            }:
                logger.info(
                    "Research agent finished for task %s",
                    task_id,
                )