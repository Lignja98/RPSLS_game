"""
Database configuration for the game history service.
"""

from typing import AsyncGenerator
import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

# ---------------------------------------------------------------------------
# Database URL
# ---------------------------------------------------------------------------
# If a DATABASE_URL env-var is provided we use it (e.g. a real Postgres
# connection string when running inside Docker-Compose or CI). For local
# hacking we fall back to a file-based SQLite database living in the project
# root – that way the service starts without any external dependencies.

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./game_history.db",  # default for local dev
)

# extra connect args are only required by SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# ---------------------------------------------------------------------------
# SQLAlchemy async engine
# ---------------------------------------------------------------------------

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    future=True,
    poolclass=NullPool,
    connect_args=connect_args,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI to get a database session."""
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


# Import models here to ensure they're registered with SQLAlchemy
from .models import Base  # noqa: E402

# Create all tables on startup
async def create_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    """Dispose the database engine."""
    await engine.dispose()


async def init_db() -> None:
    """Initialize the database, creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose() 