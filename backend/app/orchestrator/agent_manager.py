from app.agents.base_agent import BaseAgent
from app.agents.competitor_agent import CompetitorAgent
from app.agents.content_agent import ContentAgent
from app.agents.creative_agent import CreativeAgent
from app.agents.keyword_agent import KeywordAgent
from app.agents.research_agent import ResearchAgent
from app.agents.linkedin_agent import LinkedInAgent

AGENT_CLASSES: dict[
    str,
    type[BaseAgent],
] = {
    "research": ResearchAgent,
    "competitor": CompetitorAgent,
    "keyword": KeywordAgent,
    "content": ContentAgent,
    "creative": CreativeAgent,
    "linkedin": LinkedInAgent,
}


class AgentManager:

    def __init__(self) -> None:

        self._active_agents: dict[
            str,
            BaseAgent,
        ] = {}

    def create_agent(
        self,
        agent_name: str,
    ) -> BaseAgent:

        agent_class = (
            AGENT_CLASSES.get(
                agent_name
            )
        )

        if agent_class is None:

            raise ValueError(
                f"Agent '{agent_name}' "
                f"is not implemented."
            )

        return agent_class()

    def register_active(
        self,
        task_id: str,
        agent: BaseAgent,
    ) -> None:

        self._active_agents[
            task_id
        ] = agent

    def get_active(
        self,
        task_id: str,
    ) -> BaseAgent | None:

        return self._active_agents.get(
            task_id
        )

    async def remove_active(
        self,
        task_id: str,
    ) -> None:

        self._active_agents.pop(
            task_id,
            None,
        )

    async def cancel(
        self,
        task_id: str,
    ) -> bool:

        agent = self._active_agents.get(
            task_id
        )

        if agent is None:
            return False

        await agent.cancel()

        return True