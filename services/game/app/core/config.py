"""Centralised application configuration.

All runtime settings are sourced from environment variables (or an optional
`.env` file) and exposed via a cached `get_settings()` helper so the rest of
 the codebase can simply do:

    from app.core.config import get_settings
    settings = get_settings()
"""

from __future__ import annotations

import os
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Any variable can be provided in the environment **or** via a `.env` file
    placed at the project root.  Pydantic will take care of parsing and type
    coercion.
    """

    # ---------------------------------------------------------------------
    # Core
    # ---------------------------------------------------------------------
    ENVIRONMENT: str = Field("local", description="Execution environment: local/staging/prod")
    DEBUG: bool = Field(False, description="Enable debug logging & hot-reload helpers")

    # ------------------------------------------------------------------––-
    # HTTP / FastAPI
    # ------------------------------------------------------------------––-
    APP_NAME: str = Field("RPSLS Game Service", description="FastAPI application title")
    API_V1_STR: str = Field("/api/v1", description="Base prefix for V1 endpoints")
    HOST: str = Field("0.0.0.0", description="Host for Uvicorn")
    PORT: int = Field(8000, description="Port for Uvicorn")

    # ------------------------------------------------------------------––-
    # Database
    # ------------------------------------------------------------------––-
    DATABASE_URL: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", "sqlite+aiosqlite:///./game.db"
        ),
        description="SQLAlchemy compatible DSN",
    )

    # ------------------------------------------------------------------––-
    # CORS
    # ------------------------------------------------------------------––-
    ALLOWED_ORIGINS: List[str] = Field(
        default=["*"],
        description="Origins allowed for cross-origin requests",
    )

    # ------------------------------------------------------------------––-
    # Misc / Build metadata
    # ------------------------------------------------------------------––-
    VERSION: str = Field("0.1.0", description="Application version tag")

    # ------------------------------------------------------------------––-
    # Validators & configuration
    # ------------------------------------------------------------------––-
    @field_validator("VERSION", mode="before")
    @classmethod
    def _autodetect_version(cls, v: str | None):  # pragma: no cover – best-effort
        """Populate VERSION from package metadata if available."""
        if v and v != "0.1.0":
            return v
        try:
            return version("game")
        except PackageNotFoundError:
            return "0.1.0"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache
def get_settings() -> Settings:  # pragma: no cover  – called at import time
    """Return a singleton *Settings* instance.

    Using `lru_cache()` ensures that *all* imports across the codebase get the
    same object, so we don't repeatedly read the environment or parse the .env
    file.
    """

    return Settings() 