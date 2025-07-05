import importlib
from types import ModuleType

import pytest

from app.core import config as cfg


def _fresh_settings(monkeypatch: pytest.MonkeyPatch, **env) -> cfg.Settings:
    """Return a fresh Settings instance isolated from previous state.

    1. Clear any cached instance held by `get_settings`.
    2. Manipulate the process environment as requested.
    3. Reload the *config* module so Pydantic re-evaluates env vars.
    """

    # 1. Clear cache – lru_cache adds a .cache_clear() helper
    cfg.get_settings.cache_clear()

    # 2. Apply environment mutations
    monkeypatch.delenv("DATABASE_URL", raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    # 3. Reload the module so BaseSettings picks up env changes
    importlib.reload(cfg)

    return cfg.get_settings()


def test_default_sqlite(monkeypatch: pytest.MonkeyPatch):
    """Without DATABASE_URL the service should fall back to local SQLite."""

    settings = _fresh_settings(monkeypatch)
    assert settings.DATABASE_URL.startswith("sqlite+aiosqlite")


def test_custom_database_url(monkeypatch: pytest.MonkeyPatch):
    """If DATABASE_URL is set it should be honoured verbatim."""

    dsn = "postgresql+asyncpg://user:pass@db:5432/rpsls_test"
    settings = _fresh_settings(monkeypatch, DATABASE_URL=dsn)
    assert settings.DATABASE_URL == dsn


def test_version_is_non_empty(monkeypatch: pytest.MonkeyPatch):
    """VERSION field should always resolve to a non-empty string."""

    settings = _fresh_settings(monkeypatch)
    assert isinstance(settings.VERSION, str) and settings.VERSION
