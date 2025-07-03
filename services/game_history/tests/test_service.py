import pytest
from datetime import datetime, timedelta, UTC
from services.game_history.app.service import GameHistoryService
from services.game_history.app.models import GameHistory, GameHistoryCreate, GameHistoryFilter
from shared.models import Choice, GameResult, PlayerStats

@pytest.mark.asyncio
async def test_create_game_record(test_session):
    """Test creating a new game record."""
    service = GameHistoryService(test_session)
    game_data = GameHistoryCreate(
        player_id=1,
        player_choice=Choice.ROCK,
        computer_choice=Choice.SCISSORS,
        result=GameResult.WIN,
        winning_move="Rock crushes Scissors"
    )
    
    game_id = await service.create_game_record(game_data)
    created = await service.get_game_record(game_id)
    assert created.player_id == game_data.player_id
    assert created.player_choice == game_data.player_choice
    assert created.computer_choice == game_data.computer_choice
    assert created.result == game_data.result

@pytest.mark.asyncio
async def test_get_game_record(test_session, sample_game_history):
    """Test retrieving a game record."""
    service = GameHistoryService(test_session)
    game = await service.get_game_record(sample_game_history.id)
    assert game is not None
    assert game.id == sample_game_history.id
    assert game.player_id == sample_game_history.player_id

@pytest.mark.asyncio
async def test_list_games(test_session, sample_game_history):
    """Test listing games with filters."""
    service = GameHistoryService(test_session)
    
    # Test without filters
    games, total = await service.list_games()
    assert total > 0
    assert len(games) > 0
    
    # Test with player filter
    games, total = await service.list_games(player_id=sample_game_history.player_id)
    assert len(games) > 0
    assert all(g.player_id == sample_game_history.player_id for g in games)
    
    # Test with result filter
    games, total = await service.list_games(result=sample_game_history.result.value)
    assert len(games) > 0
    assert all(g.result == sample_game_history.result for g in games)

@pytest.mark.asyncio
async def test_get_player_stats(test_session, sample_game_history):
    """Test getting player statistics."""
    service = GameHistoryService(test_session)
    stats = await service.get_player_stats(sample_game_history.player_id)
    
    assert stats is not None
    assert isinstance(stats, PlayerStats)
    assert sum(stats.stats.values()) >= 1

@pytest.mark.asyncio
async def test_cleanup_old_records(test_session):
    """Test cleaning up old records."""
    service = GameHistoryService(test_session)
    
    # Create an old game record
    old_game = GameHistory(
        player_id=1,
        player_choice=Choice.ROCK,
        computer_choice=Choice.SCISSORS,
        result=GameResult.WIN,
        winning_move="Rock crushes Scissors",
        played_at=datetime.now(UTC) - timedelta(days=31)  # 31 days old
    )
    test_session.add(old_game)
    await test_session.commit()
    
    # Clean up games older than 30 days
    deleted_count = await service.cleanup_old_records(days=30)
    assert deleted_count >= 1  # Should have deleted at least our test record 