import logging

from fastapi import FastAPI

from app.agents.agent_registry import AGENT_DEFINITIONS
from app.config import get_settings
from app.api.routes import (
    agents,
    amy,
    analytics,
    calendar,
    competitors,
    content,
    creative,
    health,
    keywords,
    linkedin,
    memory,
    research,
    settings,
    tasks,
    voice,
)
from app.api.websocket import router as websocket_router
from app.middleware import (
    AMYException,
    amy_exception_handler,
    configure_cors,
    unhandled_exception_handler,
)
from app.services.agent_initializer import initialize_agents
from app.utils.logging import configure_logging


settings_config = get_settings()

configure_logging(
    settings_config.log_level
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="CTons AMY API",
    description=(
        "CTons AMY local AI "
        "LinkedIn operating system."
    ),
    version="0.1.0",
)


configure_cors(app)

app.add_exception_handler(
    AMYException,
    amy_exception_handler,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)


app.include_router(
    health.router,
    prefix="/api",
)

app.include_router(
    agents.router,
    prefix="/api",
)

app.include_router(
    tasks.router,
    prefix="/api",
)

app.include_router(
    amy.router,
    prefix="/api",
)

app.include_router(
    research.router,
    prefix="/api",
)

app.include_router(
    competitors.router,
    prefix="/api",
)

app.include_router(
    keywords.router,
    prefix="/api",
)

app.include_router(
    content.router,
    prefix="/api",
)

app.include_router(
    creative.router,
    prefix="/api",
)

app.include_router(
    linkedin.router,
    prefix="/api",
)

app.include_router(
    calendar.router,
    prefix="/api",
)

app.include_router(
    analytics.router,
    prefix="/api",
)

app.include_router(
    memory.router,
    prefix="/api",
)

app.include_router(
    settings.router,
    prefix="/api",
)

app.include_router(
    voice.router,
    prefix="/api",
)

app.include_router(
    websocket_router
)


@app.on_event("startup")
async def startup_event():

    initialize_agents()

    logger.info(
        "CTons AMY started."
    )

    logger.info(
        "Mock mode: %s",
        settings_config.mock_mode,
    )

    logger.info(
        "Registered agents: %s",
        len(AGENT_DEFINITIONS),
    )


@app.get("/")
async def root():

    return {
        "success": True,
        "data": {
            "application": "CTons AMY",
            "status": "online",
            "version": "0.1.0",
            "storage": "in_memory",
            "docs": "/docs",
        },
    }