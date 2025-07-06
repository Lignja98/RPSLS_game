from __future__ import annotations

"""Play endpoint - executes a game round."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.repositories.game_repository import GameRepository
from app.schemas.game import PlayRequest, PlayResponse
from app.services.game_service import GameService

router = APIRouter()


@router.post(
    "/play",
    response_model=PlayResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Play a round against the computer",
)
async def play_round(
    payload: PlayRequest,
    session: AsyncSession = Depends(get_db_session),
) -> PlayResponse:
    """Execute a single round and persist the outcome."""

    repo = GameRepository(session)
    service = GameService(repo)
    game = await service.play(payload.to_choice())
    return PlayResponse.from_round(
        game.player_choice, game.computer_choice, game.winner
    )
