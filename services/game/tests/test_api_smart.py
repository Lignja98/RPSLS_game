from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.db.database import Base, get_db_session
from app.utils.enums import Choice, Mode
import app.utils.ai as ai_mod
from app.main import app as fastapi_app
from collections.abc import AsyncIterator


@pytest.fixture(name="client_smart")
async def _client_fixture() -> AsyncIterator[AsyncClient]:
    """Provide an httpx client backed by an isolated in-memory DB for smart tests."""

    test_engine: AsyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        test_engine, expire_on_commit=False, autoflush=False
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def _get_test_session() -> AsyncIterator[AsyncSession]:  # noqa: D401
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:  # noqa: BLE001 – re-raise after rollback
                await session.rollback()
                raise

    fastapi_app.dependency_overrides[get_db_session] = _get_test_session

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    fastapi_app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.mark.asyncio
async def test_play_smart_mode(
    client_smart: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    """Smart mode should forward through the stack and use ai.smart_choice result."""

    # Monkeypatch smart_choice to deterministic return
    monkeypatch.setattr(
        ai_mod, "smart_choice", lambda _hist: Choice.SPOCK, raising=True
    )

    settings = get_settings()
    prefix = settings.API_V1_STR

    # First play with smart mode (even without history)
    resp = await client_smart.post(
        f"{prefix}/play",
        json={"player": Choice.ROCK.value, "mode": Mode.SMART.value},
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["player"] == Choice.ROCK.value
    assert data["computer"] == Choice.SPOCK.value
