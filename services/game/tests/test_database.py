from app.db.database import get_db_session
import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_db_session_smoke():
    """Ensure the DB engine & session factory are wired correctly.

    Uses the in-memory SQLite fallback (or whatever DATABASE_URL points to)
    to execute a trivial query.  Acts as a fast smoke test rather than a full
    integration test.
    """

    async with get_db_session() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar_one() == 1
