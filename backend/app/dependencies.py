from functools import lru_cache

from app.agents import AGENT_DEFINITIONS
from app.config import Settings, get_settings
from app.orchestrator import AgentManager, CommandRouter, WorkflowEngine


@lru_cache
def get_command_router() -> CommandRouter:
    return CommandRouter()


@lru_cache
def get_agent_manager() -> AgentManager:
    return AgentManager()


@lru_cache
def get_workflow_engine() -> WorkflowEngine:
    return WorkflowEngine()


def get_app_settings() -> Settings:
    return get_settings()


def get_agent_definitions():
    return AGENT_DEFINITIONS