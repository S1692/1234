"""Database setup and session handling for the service."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from .config import get_settings

Base = declarative_base()

# Load settings
_settings = get_settings()

# Convert to asyncpg-compatible URL
raw_url = _settings.database_url
if raw_url.startswith("postgresql://"):
    raw_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create the async engine using the converted database URL
engine = create_async_engine(
    raw_url,
    echo=False,
    pool_pre_ping=True,
)

# Sessionmaker for dependency injection
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async with async_session() as session:
        yield session

async def init_db() -> None:
    """
    Create database tables if they do not exist. This function should be
    called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
