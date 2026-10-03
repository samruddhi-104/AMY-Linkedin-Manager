AGENT_PERMISSIONS: dict[str, set[str]] = {
    "research": {
        "WEB_SEARCH",
        "WEB_FETCH",
        "MEMORY_READ",
        "MEMORY_WRITE",
    },
    "competitor": {
        "WEB_SEARCH",
        "WEB_FETCH",
        "MEMORY_READ",
        "MEMORY_WRITE",
    },
    "keyword": {
        "WEB_SEARCH",
        "MEMORY_READ",
        "MEMORY_WRITE",
    },
    "content": {
        "MEMORY_READ",
        "MEMORY_WRITE",
        "CONTENT_GENERATE",
    },
    "creative": {
        "IMAGE_GENERATE",
        "ASSET_WRITE",
    },
    "linkedin": {
        "LINKEDIN_READ",
        "LINKEDIN_PUBLISH",
    },
    "analytics": {
        "ANALYTICS_READ",
        "MEMORY_WRITE",
    },
}


def can_agent_use_tool(
    agent_name: str,
    permission: str,
) -> bool:
    return permission in AGENT_PERMISSIONS.get(
        agent_name,
        set(),
    )