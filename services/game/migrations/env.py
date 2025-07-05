from __future__ import annotations

import asyncio
import sys
import logging
from logging.config import fileConfig
from pathlib import Path
from typing import cast

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config
from sqlalchemy.engine import Connection

# Ensure project "app" package is importable when Alembic runs standalone.
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # .../services/game
sys.path.append(str(PROJECT_ROOT))

from app.core.config import get_settings
from app.db.database import Base, engine as sa_engine


# ---------------------------------------------------------------------------
# Alembic configuration
# ---------------------------------------------------------------------------
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger(__name__)

# Inject our database URL – avoids duplicating it in alembic.ini
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Make metadata available to autogenerate migrations
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# Helper routines
# ---------------------------------------------------------------------------


def run_migrations_offline() -> None:  # noqa: D401 – imperative mood
    """Run migrations in *offline* mode."""

    url = cast(str, config.get_main_option("sqlalchemy.url"))
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:  # noqa: D401 – imperative mood
    """Run migrations in *online* mode."""

    connectable: AsyncEngine = sa_engine

    async def run_async_migrations() -> None:  # noqa: D401 – imperative mood
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
