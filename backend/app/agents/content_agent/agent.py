import logging
import time
from typing import Any
from uuid import uuid4

from app.agents.base_agent import BaseAgent
from app.agents.content_agent.prompts import SYSTEM_PROMPT
from app.agents.content_agent.schemas import ContentResult
from app.config import get_settings
from app.providers.factory import get_openai_provider
from app.services.in_memory_store import store
from app.services.memory_service import memory_service


logger = logging.getLogger(__name__)


CONTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "content_type": {
            "type": "string",
        },
        "title": {
            "type": "string",
        },
        "hook": {
            "type": "string",
        },
        "body": {
            "type": "string",
        },
        "cta": {
            "type": "string",
        },
        "keywords": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "hashtags": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "visual_concept": {
            "type": "string",
        },
        "sources_used": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
    },
    "required": [
        "content_type",
        "title",
        "hook",
        "body",
        "cta",
        "keywords",
        "hashtags",
        "visual_concept",
        "sources_used",
    ],
    "additionalProperties": False,
}


class ContentAgent(BaseAgent):

    name = "content"

    display_name = "Content Agent"

    version = "3.0.0"

    capabilities = [
        "CONTENT_GENERATION",
        "MEMORY_READ",
        "MEMORY_WRITE",
    ]

    async def run(
        self,
        task_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:

        self.status = "RUNNING"

        start = time.perf_counter()

        topic = str(
            input_data.get(
                "topic",
                "",
            )
        ).strip()

        if not topic:

            self.status = "FAILED"

            raise ValueError(
                "A content topic is required."
            )

        try:

            settings = get_settings()

            # -------------------------------------------------
            # Get CTons profile
            # -------------------------------------------------

            profile = (
                store.get_company_profile()
            )

            # -------------------------------------------------
            # Retrieve relevant memory
            # -------------------------------------------------

            memories = memory_service.search(
                topic,
                limit=5,
            )

            memory_context = "\n\n".join(
                item["content"]
                for item in memories
            )

            # -------------------------------------------------
            # Retrieve latest research
            # -------------------------------------------------

            research_reports = (
                store.list_research()
            )

            latest_research = (
                research_reports[-1]
                if research_reports
                else None
            )

            research_context = ""

            sources = []

            if latest_research:

                research_data = (
                    latest_research.get(
                        "result",
                        {},
                    )
                )

                research_context = (
                    str(research_data)
                )

                for source in research_data.get(
                    "sources",
                    [],
                ):
                    url = source.get("url")

                    if url:
                        sources.append(url)

            # =================================================
            # MOCK MODE
            # =================================================

            if settings.mock_mode:

                result = ContentResult(
                    content_type="linkedin_post",

                    title=(
                        "AI Agents Are Changing "
                        "How Businesses Automate Work"
                    ),

                    hook=(
                        "Most businesses don't need "
                        "more software. They need "
                        "smarter ways to connect the "
                        "software they already use."
                    ),

                    body=(
                        "AI agents are changing that.\n\n"
                        "Instead of following a fixed "
                        "automation every time, an AI agent "
                        "can understand a goal, decide which "
                        "tools to use and adapt its workflow "
                        "to the situation.\n\n"
                        "For businesses, that creates an "
                        "interesting opportunity: automate "
                        "work that previously required "
                        "human coordination.\n\n"
                        "The real value isn't AI for the sake "
                        "of AI.\n\n"
                        "It's removing repetitive work so "
                        "teams can focus on decisions, "
                        "customers and growth."
                    ),

                    cta=(
                        "Where do you think AI agents "
                        "will create the biggest impact "
                        "in business?"
                    ),

                    keywords=[
                        "AI agents",
                        "business automation",
                        "enterprise AI",
                    ],

                    hashtags=[
                        "#AI",
                        "#AIAgents",
                        "#Automation",
                        "#ArtificialIntelligence",
                    ],

                    visual_concept=(
                        "A professional visual showing "
                        "an AI agent coordinating multiple "
                        "business systems."
                    ),

                    sources_used=sources,
                )

            # =================================================
            # REAL OPENAI MODE
            # =================================================

            else:

                openai = (
                    get_openai_provider()
                )

                profile_context = f"""
COMPANY PROFILE:

Company:
{profile["company_name"]}

Description:
{profile["description"]}

Industry:
{profile["industry"]}

Target Audience:
{profile["target_audience"]}

Services:
{profile["services"]}

Content Pillars:
{profile["content_pillars"]}

Brand Voice:
{profile["brand_voice"]}

Preferred CTA:
{profile["preferred_cta"]}

Preferred Hashtags:
{profile["preferred_hashtags"]}

Visual Style:
{profile["visual_style"]}
"""

                prompt = f"""
Create one original LinkedIn post.

TOPIC:
{topic}

{profile_context}

RELEVANT MEMORY:
{memory_context}

LATEST RESEARCH:
{research_context}

Requirements:

- Strong opening hook
- Practical value
- Professional tone
- CTons perspective
- Natural language
- Useful CTA
- Relevant keywords
- Maximum five hashtags
- Visual concept
- Do not invent statistics
- Do not copy source wording
- Use research sources only as supporting context

Keep the post suitable for LinkedIn.
"""

                response = (
                    await openai.generate_json(
                        instructions=SYSTEM_PROMPT,
                        input_text=prompt,
                        schema_name="content_result",
                        schema=CONTENT_SCHEMA,
                        use_web_search=False,
                    )
                )

                result = (
                    ContentResult.model_validate(
                        response["data"]
                    )
                )

            # -------------------------------------------------
            # Store post
            # -------------------------------------------------

            post_id = str(
                uuid4()
            )

            duration_ms = int(
                (
                    time.perf_counter()
                    - start
                )
                * 1000
            )

            post = {
                "id": post_id,
                "task_id": task_id,
                "status": "DRAFT",
                **result.model_dump(),
                "created_at": time.time(),
                "duration_ms": duration_ms,
            }

            store.add_post(post)

            # -------------------------------------------------
            # Save memory
            # -------------------------------------------------

            memory_service.save(
                content=(
                    f"Generated CTons LinkedIn post "
                    f"about {topic}. "
                    f"Hook: {result.hook}"
                ),
                memory_type="past_post",
                metadata={
                    "post_id": post_id,
                    "topic": topic,
                },
            )

            self.status = "COMPLETED"

            return {
                "agent": self.name,
                "task_id": task_id,
                "status": "COMPLETED",
                "post_id": post_id,
                "duration_ms": duration_ms,
                "result": result.model_dump(),
            }

        except Exception:

            self.status = "FAILED"

            logger.exception(
                "Content agent failed for task %s",
                task_id,
            )

            raise