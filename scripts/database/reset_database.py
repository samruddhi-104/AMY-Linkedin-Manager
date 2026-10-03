import asyncio

from backend.app.database.base import Base
from backend.app.database.session import engine


async def reset_database():
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.drop_all
        )

        await connection.run_sync(
            Base.metadata.create_all
        )


if __name__ == "__main__":
    asyncio.run(reset_database())