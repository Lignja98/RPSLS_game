import pytest
from datetime import datetime, UTC
from services.game_history.app.models import GameHistory
from shared.models import Choice, GameResult

def test_game_history_creation():
    """Test creating a GameHistory instance with valid data."""
    game = GameHistory(
        player_id=1,
        player_choice=Choice.ROCK,
        computer_choice=Choice.SCISSORS,
        result=GameResult.WIN,
        winning_move="Rock crushes Scissors",
        played_at=datetime.now(UTC)
    )
    
    assert game.player_id == 1
    assert game.player_choice == Choice.ROCK
    assert game.computer_choice == Choice.SCISSORS
    assert game.result == GameResult.WIN
    assert game.winning_move == "Rock crushes Scissors"
    assert isinstance(game.played_at, datetime)

def test_game_history_representation():
    """Test the string representation of GameHistory."""
    game = GameHistory(
        player_id=1,
        player_choice=Choice.ROCK,
        computer_choice=Choice.SCISSORS,
        result=GameResult.WIN,
        winning_move="Rock crushes Scissors",
        played_at=datetime.now(UTC)
    )
    
    # Check that the string representation contains key information
    str_repr = str(game)
    assert str(game.id) in str_repr
    assert str(game.player_id) in str_repr
    assert game.result.value in str_repr

@pytest.mark.parametrize("invalid_data", [
    {"player_id": None},  # Missing required field
    {"player_choice": "INVALID"},  # Invalid move
    {"result": "INVALID"},  # Invalid result
])
def test_game_history_invalid_data(invalid_data):
    """Test creating GameHistory with invalid data raises appropriate errors."""
    valid_data = {
        "player_id": 1,
        "player_choice": Choice.ROCK,
        "computer_choice": Choice.SCISSORS,
        "result": GameResult.WIN,
        "winning_move": "Rock crushes Scissors",
        "played_at": datetime.now(UTC)
    }
    
    # Update valid data with invalid data
    test_data = valid_data.copy()
    test_data.update(invalid_data)
    
    with pytest.raises(Exception):  # Will raise SQLAlchemy or validation error
        GameHistory(**test_data) 