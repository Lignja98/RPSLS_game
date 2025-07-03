"""
Repository layer for database operations.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.orm import validates

from shared.models import GameResult
from .models import GameHistory, GameHistoryFilter


class GameHistoryRepository:
    """Repository for game history operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, game: GameHistory) -> GameHistory:
        """Create a new game history record."""
        self._session.add(game)
        await self._session.flush()
        await self._session.refresh(game)
        return game

    async def get_by_id(self, game_id: int) -> Optional[GameHistory]:
        """Get a game by ID."""
        stmt = select(GameHistory).where(GameHistory.id == game_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    def _build_filter_query(self, filter_params: GameHistoryFilter) -> Select:
        """Build a query based on filter parameters."""
        query = select(GameHistory)

        if filter_params.player_id is not None:
            query = query.where(GameHistory.player_id == filter_params.player_id)
        
        if filter_params.result is not None:
            query = query.where(GameHistory.result == filter_params.result)
        
        if filter_params.from_date is not None:
            query = query.where(GameHistory.played_at >= filter_params.from_date)
        
        if filter_params.to_date is not None:
            query = query.where(GameHistory.played_at <= filter_params.to_date)
        
        # Always sort by most recent first
        query = query.order_by(GameHistory.played_at.desc())
        
        # Add pagination
        query = query.offset(filter_params.offset).limit(filter_params.limit)
        
        return query

    async def list_games(
        self,
        player_id: Optional[int] = None,
        result: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[GameHistory], int]:
        """List games with optional filters."""
        # Build query conditions
        conditions = []
        if player_id is not None:
            conditions.append(GameHistory.player_id == player_id)
        if result is not None:
            try:
                game_result = GameResult(result)
                conditions.append(GameHistory.result == game_result)
            except ValueError:
                # Invalid result value, return empty list
                return [], 0

        # Count total matching records
        count_stmt = select(func.count()).select_from(GameHistory)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        total = await self._session.scalar(count_stmt) or 0

        # Get paginated records
        stmt = (
            select(GameHistory)
            .order_by(GameHistory.played_at.desc())
            .offset(offset)
            .limit(limit)
        )
        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self._session.execute(stmt)
        games = list(result.scalars().all())
        
        # Ensure games are attached to this session
        for game in games:
            self._session.add(game)
        await self._session.flush()
        
        return games, total

    async def get_player_stats(self, player_id: int) -> Dict[GameResult, int]:
        """Get game statistics for a player."""
        stmt = (
            select(GameHistory.result, func.count())
            .where(GameHistory.player_id == player_id)
            .group_by(GameHistory.result)
        )
        result = await self._session.execute(stmt)
        stats = dict(result.all())
        
        # Ensure all results have a count
        return {
            result: stats.get(result, 0)
            for result in GameResult
        }

    async def delete_old_games(self, cutoff_date: datetime) -> int:
        """Delete games older than cutoff_date."""
        stmt = (
            select(GameHistory)
            .where(GameHistory.played_at < cutoff_date)
        )
        result = await self._session.execute(stmt)
        games = result.scalars().all()
        
        for game in games:
            await self._session.delete(game)
        await self._session.flush()
        
        return len(games) 