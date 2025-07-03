import pytest
from datetime import datetime, timedelta, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from services.game_history.app.repository import GameHistoryRepository
from services.game_history.app.models import GameHistory, GameHistoryFilter
from shared.models import Choice, GameResult

@pytest.mark.asyncio
async def test_create_game_history(test_session):
    """Test creating a new game history record."""
    repo = GameHistoryRepository(test_session)
    game = GameHistory(
        player_id=1,
        player_choice=Choice.PAPER,
        computer_choice=Choice.ROCK,
        result=GameResult.WIN,
        winning_move="Paper covers Rock",
        played_at=datetime.now(UTC)
    )
    
    created_game = await repo.create(game)
    assert created_game.player_id == 1
    assert created_game.player_choice == Choice.PAPER
    assert created_game.computer_choice == Choice.ROCK
    assert created_game.result == GameResult.WIN

@pytest.mark.asyncio
async def test_get_game_history(test_session, sample_game_history):
    """Test retrieving a game history record by ID."""
    repo = GameHistoryRepository(test_session)
    game = await repo.get_by_id(sample_game_history.id)
    assert game is not None
    assert game.id == sample_game_history.id
    assert game.player_id == sample_game_history.player_id

@pytest.mark.asyncio
async def test_get_nonexistent_game_history(test_session):
    """Test retrieving a non-existent game history record."""
    repo = GameHistoryRepository(test_session)
    game = await repo.get_by_id(999)
    assert game is None

@pytest.mark.asyncio
async def test_list_game_history(test_session, sample_game_history):
    """Test listing game history records with filters."""
    repo = GameHistoryRepository(test_session)
    
    # Test without filters
    games, total = await repo.list_games()
    assert len(games) > 0
    
    # Test with player filter
    games, total = await repo.list_games(player_id=sample_game_history.player_id)
    assert len(games) > 0
    assert all(g.player_id == sample_game_history.player_id for g in games)
    
    # Test with result filter
    games, total = await repo.list_games(result=sample_game_history.result.value)
    assert len(games) > 0
    assert all(g.result == sample_game_history.result for g in games)

@pytest.mark.asyncio
async def test_get_player_statistics(test_session, sample_game_history):
    """Test getting player statistics."""
    repo = GameHistoryRepository(test_session)
    stats = await repo.get_player_stats(sample_game_history.player_id)
    
    assert stats is not None
    assert isinstance(stats, dict)
    assert all(isinstance(key, GameResult) for key in stats.keys())
    assert all(isinstance(value, int) for value in stats.values())
    assert sum(stats.values()) >= 1  # At least one game should exist

@pytest.mark.asyncio
async def test_delete_old_games(test_session):
    """Test deleting old game records."""
    repo = GameHistoryRepository(test_session)
    cutoff_date = datetime.now(UTC) - timedelta(days=30)
    deleted_count = await repo.delete_old_games(cutoff_date)
    assert isinstance(deleted_count, int)  # Should return number of deleted records 