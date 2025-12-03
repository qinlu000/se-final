import os
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_SQLITE_URL = f"sqlite+aiosqlite:///{BASE_DIR / 'app.db'}"

# Use DATABASE_URL env var when provided, otherwise fall back to a local SQLite file.
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
