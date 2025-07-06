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
from app.utils.enums import Choice
import app.services.game_service as gs
from app.main import app as fastapi_app
from collections.abc import AsyncIterator


@pytest.fixture(name="client")
async def _client_fixture() -> AsyncIterator[AsyncClient]:
    """Provide an *httpx* client backed by an isolated in-memory DB."""

    test_engine: AsyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        test_engine, expire_on_commit=False, autoflush=False
    )

    # Create schema in the in-memory DB
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

    # Override dependency
    fastapi_app.dependency_overrides[get_db_session] = _get_test_session

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    fastapi_app.dependency_overrides.clear()

    # Ensure all connections are cleaned up to avoid AsyncSession.close warnings
    await test_engine.dispose()


@pytest.mark.asyncio
async def test_choices_endpoints(client: AsyncClient):
    settings = get_settings()
    prefix = settings.API_V1_STR

    resp = await client.get(f"{prefix}/choices")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 5
    assert {item["id"] for item in data} == {1, 2, 3, 4, 5}

    resp_rand = await client.get(f"{prefix}/choice")
    assert resp_rand.status_code == 200
    rand_choice = resp_rand.json()
    assert 1 <= rand_choice["id"] <= 5


@pytest.mark.asyncio
async def test_play_and_history_endpoints(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    settings = get_settings()
    prefix = settings.API_V1_STR

    # Patch randomness for determinism
    async def _fixed_random_choice() -> Choice:  # noqa: D401
        return Choice.PAPER

    monkeypatch.setattr(gs, "random_choice", _fixed_random_choice, raising=True)

    # Play one round
    resp = await client.post(f"{prefix}/play", json={"player": Choice.ROCK.value})
    assert resp.status_code == 201
    body = resp.json()
    assert body["player"] == Choice.ROCK.value
    assert body["computer"] == Choice.PAPER.value
    assert body["results"] in {"win", "lose", "tie"}

    # Scoreboard should list the game
    history = await client.get(f"{prefix}/history?limit=10")
    assert history.status_code == 200
    hist_data = history.json()
    assert len(hist_data) == 1

    # Clear scoreboard
    del_resp = await client.delete(f"{prefix}/history")
    assert del_resp.status_code == 204

    history_after = await client.get(f"{prefix}/history")
    assert history_after.status_code == 200
    assert history_after.json() == []
