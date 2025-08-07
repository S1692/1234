"""Database setup and session handling for the service (Supabase Pooler 대응)."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from .config import get_settings

# Declare base class for SQLAlchemy models
Base = declarative_base()

# Load environment-based settings
_settings = get_settings()

# ✅ Convert to asyncpg-compatible scheme
db_url = _settings.database_url
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# ✅ Create async engine (Supabase Shared Pooler 대응: disable statement cache)
engine = create_async_engine(
    db_url,
    echo=False,
    pool_pre_ping=True,
    connect_args={"statement_cache_size": 0},  # 🔥 핵심 설정
)

# ✅ Async session factory for DI
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# ✅ Dependency for FastAPI route injection
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# ✅ Init DB: Run on startup
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

