from __future__ import annotations

"""Game history / scoreboard endpoints."""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.repositories.game_repository import GameRepository
from app.schemas.game import GameRead

router = APIRouter()

_DEFAULT_LIMIT = 10
_MAX_LIMIT = 100


@router.get(
    "/history",
    response_model=list[GameRead],
    summary="Return most recent games (scoreboard)",
)
async def list_history(
    limit: int = Query(
        _DEFAULT_LIMIT, ge=1, le=_MAX_LIMIT, description="Number of records to return"
    ),
    session: AsyncSession = Depends(get_db_session),
) -> list[GameRead]:
    """Return the *limit* most recently played games."""

    repo = GameRepository(session)
    games = await repo.list_recent(limit)
    return [GameRead.from_model(g) for g in games]


@router.delete(
    "/history",
    summary="Clear the scoreboard (delete all games)",
)
async def clear_history(session: AsyncSession = Depends(get_db_session)) -> Response:
    """Delete all game records and respond with *204 No Content*."""

    repo = GameRepository(session)
    await repo.clear()

    # Return an explicit empty 204 response to satisfy FastAPI's body restrictions.
    return Response(status_code=status.HTTP_204_NO_CONTENT)
