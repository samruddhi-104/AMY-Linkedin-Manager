from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.agent_registry import AGENT_DEFINITIONS
from app.database.base import Base
from app.database.session import AsyncSessionLocal, engine
from app.models import Agent


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )


async def seed_agents(
    session: AsyncSession,
) -> None:
    for definition in AGENT_DEFINITIONS:
        existing = await session.execute(
            select(Agent).where(
                Agent.name == definition["name"]
            )
        )

        agent = existing.scalar_one_or_none()

        if agent is None:
            session.add(
                Agent(
                    name=definition["name"],
                    display_name=definition["display_name"],
                    description=definition["description"],
                    version=definition["version"],
                    status=definition["status"],
                    enabled=definition["enabled"],
                    capabilities=definition["capabilities"],
                )
            )

    await session.commit()


async def initialize_database() -> None:
    await create_tables()

    async with AsyncSessionLocal() as session:
        await seed_agents(session)