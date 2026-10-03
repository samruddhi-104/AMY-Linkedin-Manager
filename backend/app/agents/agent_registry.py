from app.tasks.task_states import AgentStatus


AGENT_DEFINITIONS = [

    {
        "name": "research",
        "display_name": "Research Agent",
        "description": (
            "Researches topics and gathers "
            "structured evidence."
        ),
        "version": "2.0.0",
        "status": AgentStatus.IDLE.value,
        "enabled": True,
        "capabilities": [
            "WEB_SEARCH",
            "WEB_FETCH",
            "RESEARCH",
        ],
    },

    {
        "name": "competitor",
        "display_name": "Competitor Intelligence Agent",
        "description": (
            "Analyzes competitors and "
            "publicly available content."
        ),
        "version": "2.0.0",
        "status": AgentStatus.IDLE.value,
        "enabled": True,
        "capabilities": [
            "WEB_SEARCH",
            "WEB_FETCH",
            "COMPETITOR_RESEARCH",
        ],
    },

    {
        "name": "keyword",
        "display_name": "Keyword Agent",
        "description": (
            "Researches keywords and hashtags."
        ),
        "version": "2.0.0",
        "status": AgentStatus.IDLE.value,
        "enabled": True,
        "capabilities": [
            "WEB_SEARCH",
            "KEYWORD_RESEARCH",
            "HASHTAG_RESEARCH",
        ],
    },

    {
        "name": "content",
        "display_name": "Content Agent",
        "description": (
            "Creates original LinkedIn content "
            "using research and brand memory."
        ),
        "version": "3.0.0",
        "status": AgentStatus.IDLE.value,
        "enabled": True,
        "capabilities": [
            "CONTENT_GENERATION",
            "MEMORY_READ",
            "MEMORY_WRITE",
        ],
    },

    {
        "name": "creative",
        "display_name": "Creative Agent",
        "description": (
            "Creates professional visual assets "
            "for LinkedIn posts."
        ),
        "version": "3.0.0",
        "status": AgentStatus.IDLE.value,
        "enabled": True,
        "capabilities": [
            "IMAGE_GENERATION",
            "ASSET_WRITE",
        ],
    },

    {
        "name": "linkedin",
        "display_name": "LinkedIn Agent",
        "description": (
            "Publishes and schedules "
            "approved LinkedIn content."
        ),
        "version": "1.0.0",
        "status": AgentStatus.IDLE.value,
        "enabled": False,
        "capabilities": [
            "LINKEDIN_READ",
            "LINKEDIN_PUBLISH",
            "LINKEDIN_SCHEDULE",
        ],
    },

    {
        "name": "analytics",
        "display_name": "Analytics Agent",
        "description": (
            "Analyzes available content "
            "performance data."
        ),
        "version": "1.0.0",
        "status": AgentStatus.IDLE.value,
        "enabled": False,
        "capabilities": [
            "ANALYTICS_READ",
        ],
    },
]