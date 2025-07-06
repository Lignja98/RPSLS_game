"""Database layer boilerplate: engine, session factory, and Base class.

All other modules should import *only* the items exposed in ``__all__`` to avoid
coupling to SQLAlchemy internals.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

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
    echo=False,  # disable raw SA echo; we implement structured timing below
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
async def get_db_session() -> AsyncIterator[AsyncSession]:  # noqa: D401 – imperative mood for FastAPI Depends
    """Provide an *AsyncSession* for a single request.

    Usage:
        async def endpoint(session: AsyncSession = Depends(get_db_session)):
            ...
    The session is committed if the request handler exits without exceptions;
    otherwise it rolls back.
    """

    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:  # noqa: BLE001 – re-raise after rollback
            await session.rollback()
            raise


# ---------------------------------------------------------------------------
# Optional query timing when DEBUG flag is set
# ---------------------------------------------------------------------------

if settings.DEBUG:
    import time
    import structlog
    from typing import Any
    from sqlalchemy import event

    _sqllog = structlog.get_logger("sqlalchemy")

    @event.listens_for(engine.sync_engine, "before_cursor_execute")
    def _before_cursor_execute(
        _conn: Any,
        _cursor: Any,
        _statement: str,
        _parameters: Any,
        context: Any,
        _executemany: bool,
    ) -> None:
        context._query_start_time = time.perf_counter()

    @event.listens_for(engine.sync_engine, "after_cursor_execute")
    def _after_cursor_execute(
        _conn: Any,
        _cursor: Any,
        statement: str,
        _parameters: Any,
        context: Any,
        _executemany: bool,
    ) -> None:
        duration_ms = (time.perf_counter() - context._query_start_time) * 1000.0
        _sqllog.debug(
            "sql",
            sql=statement.strip().replace("\n", " ")[:500],
            duration_ms=round(duration_ms, 3),
        )
