import logging
import time
from typing import Any

from app.agents.base_agent import BaseAgent
from app.agents.competitor_agent.prompts import SYSTEM_PROMPT
from app.agents.competitor_agent.schemas import (
    CompetitorResearchResult,
    CompetitorObservation,
)
from app.config import get_settings
from app.providers.factory import (
    get_openai_provider,
    get_search_provider,
)


logger = logging.getLogger(__name__)


COMPETITOR_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
        },
        "observations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "competitor": {
                        "type": "string",
                    },
                    "topics": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                    "content_formats": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                    "hook_patterns": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                    "cta_patterns": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                    "positioning": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                    "opportunities_for_ctons": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                },
                "required": [
                    "competitor",
                    "topics",
                    "content_formats",
                    "hook_patterns",
                    "cta_patterns",
                    "positioning",
                    "opportunities_for_ctons",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "summary",
        "observations",
    ],
    "additionalProperties": False,
}


class CompetitorAgent(BaseAgent):

    name = "competitor"
    display_name = "Competitor Intelligence Agent"
    version = "2.0.0"

    capabilities = [
        "WEB_SEARCH",
        "WEB_FETCH",
        "COMPETITOR_RESEARCH",
    ]

    async def run(
        self,
        task_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        self.status = "RUNNING"

        competitors = input_data.get(
            "competitors",
            [],
        )

        topic = str(
            input_data.get(
                "topic",
                "AI and business automation",
            )
        )

        if not competitors:
            competitors = [
                "AI automation companies",
                "enterprise AI companies",
            ]

        start = time.perf_counter()

        try:

            search_provider = get_search_provider()

            all_results = []

            for competitor in competitors:

                query = (
                    f"{competitor} "
                    f"{topic} LinkedIn content"
                )

                results = await search_provider.search(
                    query
                )

                all_results.extend(
                    results
                )

            research_context = "\n\n".join(
                str(result)
                for result in all_results
            )

            settings = get_settings()

            if settings.mock_mode:

                result = CompetitorResearchResult(
                    summary=(
                        "Mock competitor analysis "
                        "completed."
                    ),
                    observations=[
                        CompetitorObservation(
                            competitor=competitor,
                            topics=[
                                "AI agents",
                                "automation",
                            ],
                            content_formats=[
                                "carousel",
                                "text post",
                            ],
                            hook_patterns=[
                                "Industry trend hook",
                                "Problem-based hook",
                            ],
                            cta_patterns=[
                                "Ask a question",
                                "Invite discussion",
                            ],
                            positioning=[
                                "AI innovation",
                                "Business automation",
                            ],
                            opportunities_for_ctons=[
                                "Create practical "
                                "implementation content."
                            ],
                        )
                        for competitor in competitors
                    ],
                )

            else:

                openai = get_openai_provider()

                prompt = f"""
Analyze these competitors:

{competitors}

Topic:

{topic}

Public research material:

{research_context}

Identify:

- recurring topics
- formats
- hooks
- CTAs
- positioning
- content gaps
- CTons opportunities
"""

                response = await openai.generate_json(
                    instructions=SYSTEM_PROMPT,
                    input_text=prompt,
                    schema_name="competitor_research_result",
                    schema=COMPETITOR_SCHEMA,
                    use_web_search=True,
                )

                result = (
                    CompetitorResearchResult.model_validate(
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
                "Competitor agent failed."
            )

            raise