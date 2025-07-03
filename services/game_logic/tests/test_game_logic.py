import pytest
from fastapi.testclient import TestClient

from services.game_logic.app.game import GameLogic, GameRound
from services.game_logic.app.main import app
from shared.models import Choice, GameResult

client = TestClient(app)


class TestGameLogic:
    """Test suite for the core game logic."""

    def test_get_valid_moves(self):
        """Test that all valid moves are returned."""
        moves = GameLogic.get_valid_moves()
        assert len(moves) == 5
        assert all(isinstance(move, Choice) for move in moves)
        assert Choice.ROCK in moves
        assert Choice.PAPER in moves
        assert Choice.SCISSORS in moves
        assert Choice.LIZARD in moves
        assert Choice.SPOCK in moves

    @pytest.mark.parametrize("p1_choice,p2_choice,expected_result,expected_move", [
        # Test all winning combinations
        (Choice.SCISSORS, Choice.PAPER, GameResult.WIN, "Scissors cuts Paper"),
        (Choice.PAPER, Choice.ROCK, GameResult.WIN, "Paper covers Rock"),
        (Choice.ROCK, Choice.LIZARD, GameResult.WIN, "Rock crushes Lizard"),
        (Choice.LIZARD, Choice.SPOCK, GameResult.WIN, "Lizard poisons Spock"),
        (Choice.SPOCK, Choice.SCISSORS, GameResult.WIN, "Spock smashes Scissors"),
        (Choice.SCISSORS, Choice.LIZARD, GameResult.WIN, "Scissors decapitates Lizard"),
        (Choice.LIZARD, Choice.PAPER, GameResult.WIN, "Lizard eats Paper"),
        (Choice.PAPER, Choice.SPOCK, GameResult.WIN, "Paper disproves Spock"),
        (Choice.SPOCK, Choice.ROCK, GameResult.WIN, "Spock vaporizes Rock"),
        (Choice.ROCK, Choice.SCISSORS, GameResult.WIN, "Rock crushes Scissors"),
        
        # Test some player 2 winning combinations (reverse of above)
        (Choice.PAPER, Choice.SCISSORS, GameResult.LOSE, "Scissors cuts Paper"),
        (Choice.ROCK, Choice.PAPER, GameResult.LOSE, "Paper covers Rock"),
        (Choice.SPOCK, Choice.PAPER, GameResult.LOSE, "Paper disproves Spock"),
        
        # Test draws
        (Choice.ROCK, Choice.ROCK, GameResult.TIE, None),
        (Choice.PAPER, Choice.PAPER, GameResult.TIE, None),
        (Choice.SCISSORS, Choice.SCISSORS, GameResult.TIE, None),
        (Choice.LIZARD, Choice.LIZARD, GameResult.TIE, None),
        (Choice.SPOCK, Choice.SPOCK, GameResult.TIE, None),
    ])
    def test_evaluate_round(self, p1_choice, p2_choice, expected_result, expected_move):
        """Test game round evaluation with various combinations."""
        game_round = GameRound(
            player_one_choice=p1_choice,
            player_two_choice=p2_choice
        )
        result = GameLogic.evaluate_round(game_round)
        assert result.result == expected_result
        assert result.winning_move == expected_move


class TestGameAPI:
    """Test suite for the game API endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_get_choices(self):
        """Test getting valid choices."""
        response = client.get("/choices")
        assert response.status_code == 200
        choices = response.json()["choices"]
        assert len(choices) == 5
        # Verify structure and values
        expected_choices = [
            {"id": 1, "name": "rock"},
            {"id": 2, "name": "paper"},
            {"id": 3, "name": "scissors"},
            {"id": 4, "name": "lizard"},
            {"id": 5, "name": "spock"}
        ]
        assert all(choice in choices for choice in expected_choices)

    def test_evaluate_valid_game(self):
        """Test evaluating a valid game round."""
        response = client.post("/evaluate", json={
            "player_one_choice": "rock",
            "player_two_choice": "scissors"
        })
        assert response.status_code == 200
        result = response.json()
        assert result["result"] == "win"
        assert result["winning_move"] == "Rock crushes Scissors"

    def test_evaluate_invalid_choice(self):
        """Test evaluating a game with invalid choice."""
        response = client.post("/evaluate", json={
            "player_one_choice": "invalid",
            "player_two_choice": "rock"
        })
        assert response.status_code == 422
        error_detail = response.json()["detail"][0]
        assert error_detail["msg"] == "Input should be 'rock', 'paper', 'scissors', 'lizard' or 'spock'" 