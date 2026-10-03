
from typing import Any
from uuid import uuid4


class InMemoryStore:
    """
    Temporary in-memory storage for CTons AMY.

    This is intentionally temporary.

    Later it will be replaced with:
        PostgreSQL
        +
        pgvector
    """

    def __init__(self) -> None:
        self.tasks: dict[str, dict[str, Any]] = {}
        self.agents: dict[str, dict[str, Any]] = {}
        self.research: list[dict[str, Any]] = []
        self.posts: list[dict[str, Any]] = []
        self.memory: list[dict[str, Any]] = []
        self.competitors: list[dict[str, Any]] = []
        self.keywords: list[dict[str, Any]] = []
        self.assets: list[dict[str, Any]] = []
        self.scheduled_posts: list[dict[str, Any]] = []
        self.linkedin_account: dict[str, Any] | None = None
        self.publish_attempts: list[dict[str, Any]] = []
        self.analytics: list[dict[str, Any]] = []

        # -----------------------------------------------------
        # Temporary CTons brand profile
        # -----------------------------------------------------

        self.company_profile: dict[str, Any] = {
            "company_name": "CTons Solutions",
            "description": (
                "CTons Solutions is a technology company "
                "focused on AI, software development, "
                "automation and digital transformation."
            ),
            "industry": "Technology",
            "target_audience": [
                "Founders",
                "CEOs",
                "CTOs",
                "Business Leaders",
                "Technology Decision Makers",
            ],
            "services": [
                "Artificial Intelligence",
                "AI Agents",
                "Business Automation",
                "Software Development",
                "Digital Transformation",
            ],
            "content_pillars": [
                "AI",
                "AI Agents",
                "Automation",
                "Software Development",
                "Business Technology",
                "Digital Transformation",
            ],
            "brand_voice": (
                "Professional, educational, practical, "
                "thought-leadership oriented and technical "
                "without being difficult to understand."
            ),
            "preferred_cta": (
                "End with a useful question or "
                "discussion-oriented CTA."
            ),
            "preferred_hashtags": [
                "#AI",
                "#ArtificialIntelligence",
                "#AIAgents",
                "#Automation",
                "#Technology",
            ],
            "topics_to_avoid": [
                "Generic motivational content",
                "Unverified statistics",
                "Fake case studies",
            ],
            "visual_style": (
                "Modern professional technology aesthetic, "
                "clean composition, premium B2B visual style."
            ),
        }

    # =========================================================
    # TASKS
    # =========================================================

    def create_task(
        self,
        command: str,
        task_type: str,
        priority: str = "normal",
    ) -> dict[str, Any]:

        task_id = str(uuid4())

        task = {
            "id": task_id,
            "command": command,
            "task_type": task_type,
            "status": "CREATED",
            "progress": 0,
            "priority": priority,
            "result": None,
            "error": None,
        }

        self.tasks[task_id] = task

        return task

    def get_task(
        self,
        task_id: str,
    ) -> dict[str, Any] | None:

        return self.tasks.get(task_id)

    def list_tasks(self) -> list[dict[str, Any]]:
        return list(self.tasks.values())

    def update_task(
        self,
        task_id: str,
        **updates: Any,
    ) -> dict[str, Any] | None:

        task = self.tasks.get(task_id)

        if task is None:
            return None

        task.update(updates)

        return task

    # =========================================================
    # AGENTS
    # =========================================================

    def add_agent(
        self,
        agent: dict[str, Any],
    ) -> None:

        self.agents[agent["name"]] = agent

    def get_agent(
        self,
        agent_name: str,
    ) -> dict[str, Any] | None:

        return self.agents.get(agent_name)

    def list_agents(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.agents.values())

    def update_agent(
        self,
        agent_name: str,
        **updates: Any,
    ) -> dict[str, Any] | None:

        agent = self.agents.get(agent_name)

        if agent is None:
            return None

        agent.update(updates)

        return agent

    # =========================================================
    # RESEARCH
    # =========================================================

    def add_research(
        self,
        research: dict[str, Any],
    ) -> None:

        self.research.append(research)

    def get_research(
        self,
        research_id: str,
    ) -> dict[str, Any] | None:

        for item in self.research:
            if item.get("id") == research_id:
                return item

        return None

    def list_research(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.research)

    # =========================================================
    # POSTS
    # =========================================================

    def add_post(
        self,
        post: dict[str, Any],
    ) -> None:

        self.posts.append(post)

    def get_post(
        self,
        post_id: str,
    ) -> dict[str, Any] | None:

        for post in self.posts:
            if post.get("id") == post_id:
                return post

        return None

    def update_post(
        self,
        post_id: str,
        **updates: Any,
    ) -> dict[str, Any] | None:

        post = self.get_post(post_id)

        if post is None:
            return None

        post.update(updates)

        return post

    def list_posts(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.posts)

    # =========================================================
    # MEMORY
    # =========================================================

    def add_memory(
        self,
        memory: dict[str, Any],
    ) -> None:

        self.memory.append(memory)

    def get_memory(
        self,
        memory_id: str,
    ) -> dict[str, Any] | None:

        for memory in self.memory:
            if memory.get("id") == memory_id:
                return memory

        return None

    def list_memory(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.memory)

    def delete_memory(
        self,
        memory_id: str,
    ) -> bool:

        original_length = len(self.memory)

        self.memory = [
            item
            for item in self.memory
            if item.get("id") != memory_id
        ]

        return len(self.memory) < original_length

    # =========================================================
    # COMPANY PROFILE
    # =========================================================

    def get_company_profile(
        self,
    ) -> dict[str, Any]:

        return self.company_profile

    def update_company_profile(
        self,
        **updates: Any,
    ) -> dict[str, Any]:

        self.company_profile.update(updates)

        return self.company_profile

    # =========================================================
    # COMPETITORS
    # =========================================================

    def add_competitor(
        self,
        competitor: dict[str, Any],
    ) -> None:

        self.competitors.append(competitor)

    def list_competitors(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.competitors)

    # =========================================================
    # KEYWORDS
    # =========================================================

    def add_keyword(
        self,
        keyword: dict[str, Any],
    ) -> None:

        self.keywords.append(keyword)

    def list_keywords(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.keywords)

    # =========================================================
    # ASSETS
    # =========================================================

    def add_asset(
        self,
        asset: dict[str, Any],
    ) -> None:

        self.assets.append(asset)

    def get_asset(
        self,
        asset_id: str,
    ) -> dict[str, Any] | None:

        for asset in self.assets:
            if asset.get("id") == asset_id:
                return asset

        return None

    def list_assets(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.assets)

    # =========================================================
    # SCHEDULED POSTS
    # =========================================================

    def add_scheduled_post(
        self,
        scheduled_post: dict[str, Any],
    ) -> None:

        self.scheduled_posts.append(scheduled_post)

    def get_scheduled_post(
        self,
        scheduled_id: str,
    ) -> dict[str, Any] | None:

        for item in self.scheduled_posts:
            if item.get("id") == scheduled_id:
                return item

        return None

    def update_scheduled_post(
        self,
        scheduled_id: str,
        **updates: Any,
    ) -> dict[str, Any] | None:

        item = self.get_scheduled_post(scheduled_id)

        if item is None:
            return None

        item.update(updates)

        return item

    def list_scheduled_posts(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.scheduled_posts)

    # =========================================================
    # LINKEDIN ACCOUNT
    # =========================================================

    def set_linkedin_account(
        self,
        account: dict[str, Any],
    ) -> None:

        self.linkedin_account = account

    def get_linkedin_account(
        self,
    ) -> dict[str, Any] | None:

        return self.linkedin_account

    # =========================================================
    # PUBLISH ATTEMPTS
    # =========================================================

    def add_publish_attempt(
        self,
        attempt: dict[str, Any],
    ) -> None:

        self.publish_attempts.append(attempt)

    def list_publish_attempts(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.publish_attempts)

    # =========================================================
    # ANALYTICS
    # =========================================================

    def add_analytics(
        self,
        record: dict[str, Any],
    ) -> None:

        self.analytics.append(record)

    def list_analytics(
        self,
    ) -> list[dict[str, Any]]:

        return list(self.analytics)


# =============================================================
# GLOBAL STORE
# =============================================================

store = InMemoryStore()