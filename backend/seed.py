import asyncio

from app.database.init_db import initialize_database


async def main():
    await initialize_database()


if __name__ == "__main__":
    asyncio.run(main())