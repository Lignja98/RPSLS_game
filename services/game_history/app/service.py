"""Game history service layer."""

from datetime import datetime, timedelta, UTC
from typing import Dict, List, Optional, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from services.game_history.app.models import GameHistory
from services.game_history.app.repository import GameHistoryRepository
from shared.models import GameHistoryEntry, GameResult, PlayerStats


class GameHistoryService:
    """Service for managing game history."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self._session = session
        self._repository = GameHistoryRepository(session)

    async def create_game_record(self, game_data: GameHistoryEntry) -> int:
        """Create a new game history record."""
        game = GameHistory(
            player_id=game_data.player_id,
            player_choice=game_data.player_choice,
            computer_choice=game_data.computer_choice,
            result=game_data.result,
            winning_move=game_data.winning_move,
            played_at=datetime.now(UTC)
        )
        created_game = await self._repository.create(game)
        return created_game.id

    async def get_game_record(self, game_id: int) -> Optional[GameHistoryEntry]:
        """Get a game history record by ID."""
        game = await self._repository.get_by_id(game_id)
        if game:
            return game.to_response()
        return None

    async def list_games(
        self,
        player_id: Optional[int] = None,
        result: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[GameHistoryEntry], int]:
        """List game history records with optional filters."""
        games, total = await self._repository.list_games(player_id, result, limit, offset)
        return [game.to_response() for game in games], total

    async def get_player_stats(self, player_id: int) -> PlayerStats:
        """Get game statistics for a player."""
        raw = await self._repository.get_player_stats(player_id)
        return PlayerStats(
            player_id=player_id,
            stats={res.value: cnt for res, cnt in raw.items()}
        )

    async def cleanup_old_records(self, days: int) -> int:
        """Delete game records older than specified days."""
        cutoff_date = datetime.now(UTC) - timedelta(days=days)
        return await self._repository.delete_old_games(cutoff_date)

    # (Legacy wrapper methods removed – tests updated to use the primary API.) 