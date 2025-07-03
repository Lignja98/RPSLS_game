"""
FastAPI application for game history service.
"""

from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import GameResult, GameHistoryEntry, PlayerStats
from .database import get_db_session, create_tables, dispose_engine, init_db, close_db
from .models import GameHistoryCreate, GameHistoryList, GameHistoryFilter
from .service import GameHistoryService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    await init_db()
    await create_tables()
    yield
    # Shutdown
    await dispose_engine()
    await close_db()


app = FastAPI(
    title="Game History Service",
    description="Service for managing game history in RPSLS game",
    version="1.0.0",
    lifespan=lifespan
)


@app.post(
    "/games",
    response_model=dict,
    summary="Record a new game",
    description="Creates a new game history entry"
)
async def create_game(
    game: GameHistoryEntry,
    session: AsyncSession = Depends(get_db_session)
) -> dict:
    """Create a new game history entry."""
    service = GameHistoryService(session)
    game_id = await service.create_game_record(game)
    return {"message": "Game history created", "id": game_id}


@app.get(
    "/games/{game_id}",
    response_model=GameHistoryEntry,
    summary="Get game by ID",
    description="Retrieves a specific game's details"
)
async def get_game(
    game_id: int,
    session: AsyncSession = Depends(get_db_session)
) -> GameHistoryEntry:
    """Get a specific game by ID."""
    service = GameHistoryService(session)
    game = await service.get_game_record(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.get(
    "/games",
    response_model=dict,
    summary="List games",
    description="Retrieves a filtered list of games"
)
async def list_games(
    player_id: Optional[int] = Query(None, description="Filter by player ID"),
    result: Optional[str] = Query(None, description="Filter by game result"),
    limit: int = Query(10, gt=0, description="Maximum number of entries to return"),
    offset: int = Query(0, ge=0, description="Number of entries to skip"),
    session: AsyncSession = Depends(get_db_session)
) -> dict:
    """List game history entries with optional filters."""
    service = GameHistoryService(session)
    games, total = await service.list_games(player_id, result, limit, offset)
    return {"total": total, "entries": games}


@app.get(
    "/players/{player_id}/stats",
    response_model=PlayerStats,
    summary="Get player statistics",
    description="Retrieves game statistics for a specific player"
)
async def get_player_stats(
    player_id: int,
    session: AsyncSession = Depends(get_db_session)
) -> PlayerStats:
    """Get statistics for a specific player."""
    service = GameHistoryService(session)
    return await service.get_player_stats(player_id)


@app.delete(
    "/games/cleanup",
    response_model=dict,
    summary="Clean up old games",
    description="Deletes games older than specified days"
)
async def cleanup_old_records(
    days: int = Query(30, gt=0, description="Delete games older than this many days"),
    session: AsyncSession = Depends(get_db_session)
) -> dict:
    """Delete old games."""
    service = GameHistoryService(session)
    deleted_count = await service.cleanup_old_records(days)
    return {
        "message": f"Deleted {deleted_count} games older than {days} days",
        "deleted_count": deleted_count
    } 