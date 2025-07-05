"""Database layer boilerplate: engine, session factory, and Base class.

All other modules should import *only* the items exposed in ``__all__`` to avoid
coupling to SQLAlchemy internals.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

__all__ = [
    "Base",
    "async_session_factory",
    "get_db_session",
    "engine",
]


class Base(DeclarativeBase):
    """Declarative base mapped superclass for all models."""


# ---------------------------------------------------------------------------
# Engine & session factory
# ---------------------------------------------------------------------------
settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# expire_on_commit=False   - don't expire objects so we can use them after commit
# autoflush=False         - let service layer decide when to flush/commit
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------
@asynccontextmanager
async def get_db_session() -> AsyncIterator[AsyncSession]:  # noqa: D401 – imperative mood for FastAPI Depends
    """Provide an *AsyncSession* for a single request.

    Usage:
        async def endpoint(session: AsyncSession = Depends(get_db_session)):
            ...
    The session is committed if the request handler exits without exceptions;
    otherwise it rolls back.
    """

    session: AsyncSession = async_session_factory()
    try:
        yield session
        await session.commit()
    except Exception:  # noqa: BLE001 – re-raise after rollback
        await session.rollback()
        raise
    finally:
        await session.close()
