from app.agents.agent_registry import AGENT_DEFINITIONS
from app.services.in_memory_store import store


def initialize_agents() -> None:
    for definition in AGENT_DEFINITIONS:

        store.add_agent(
            {
                "name": definition["name"],
                "display_name": definition["display_name"],
                "description": definition["description"],
                "version": definition["version"],
                "status": definition["status"],
                "enabled": definition["enabled"],
                "capabilities": definition["capabilities"],
            }
        )