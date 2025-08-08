import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from .config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()
_settings = get_settings()

# Centralized URL configuration is now in config.py
db_url = _settings.database_url

logger.info("Attempting to connect to the database...")

# Create engine with Supabase-recommended settings
engine = create_async_engine(
    db_url,
    echo=False,
    pool_pre_ping=True,
    connect_args={
        "statement_cache_size": 0,  # Recommended for PgBouncer
    },
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get a new database session."""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Initialize the database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)


