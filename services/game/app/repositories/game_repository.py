from __future__ import annotations

from collections.abc import Sequence
import uuid

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import Game
from app.utils.enums import Choice, GameResult


class GameRepository:  # noqa: D101 – simple data-access layer
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ---------------------------------------------------------------------
    # CRUD helpers
    # ---------------------------------------------------------------------
    async def add(
        self,
        player_choice: Choice,
        computer_choice: Choice,
        winner: GameResult,
    ) -> Game:
        """Persist a new *Game* instance and return it (uncommitted)."""

        game = Game(
            player_choice=player_choice,
            computer_choice=computer_choice,
            winner=winner,
        )
        self._session.add(game)
        await self._session.flush()
        return game

    async def get(self, game_id: uuid.UUID) -> Game | None:
        stmt = select(Game).where(Game.id == game_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_recent(self, limit: int = 50) -> Sequence[Game]:
        stmt = select(Game).order_by(Game.created_at.desc()).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def clear(self) -> None:
        """Delete all game records (scoreboard reset)."""

        await self._session.execute(text("DELETE FROM game"))
