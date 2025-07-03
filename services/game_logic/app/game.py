from typing import Dict, Set, Tuple

from pydantic import BaseModel, Field

from shared.models import Choice, GameResult


class GameRound(BaseModel):
    """Represents a single round of the game with two player choices."""
    player_one_choice: Choice = Field(..., description="First player's choice")
    player_two_choice: Choice = Field(..., description="Second player's choice")


class GameOutcome(BaseModel):
    """Represents the outcome of a game round."""
    result: GameResult = Field(..., description="The result of the game")
    winning_move: str | None = Field(None, description="Description of the winning move")


class GameLogic:
    """Core game logic for Rock Paper Scissors Lizard Spock."""

    # Define winning combinations and their descriptions
    _WINNING_MOVES: Dict[Tuple[Choice, Choice], str] = {
        (Choice.SCISSORS, Choice.PAPER): "Scissors cuts Paper",
        (Choice.PAPER, Choice.ROCK): "Paper covers Rock",
        (Choice.ROCK, Choice.LIZARD): "Rock crushes Lizard",
        (Choice.LIZARD, Choice.SPOCK): "Lizard poisons Spock",
        (Choice.SPOCK, Choice.SCISSORS): "Spock smashes Scissors",
        (Choice.SCISSORS, Choice.LIZARD): "Scissors decapitates Lizard",
        (Choice.LIZARD, Choice.PAPER): "Lizard eats Paper",
        (Choice.PAPER, Choice.SPOCK): "Paper disproves Spock",
        (Choice.SPOCK, Choice.ROCK): "Spock vaporizes Rock",
        (Choice.ROCK, Choice.SCISSORS): "Rock crushes Scissors",
    }

    @classmethod
    def get_valid_moves(cls) -> Set[Choice]:
        """Get all valid moves in the game.

        Returns:
            Set[Choice]: Set of all valid choices
        """
        return set(Choice)

    @classmethod
    def evaluate_round(cls, game_round: GameRound) -> GameOutcome:
        """Evaluate a game round and determine the winner.

        Args:
            game_round (GameRound): The game round to evaluate

        Returns:
            GameOutcome: The result of the game round
        """
        # Check for draw first
        if game_round.player_one_choice == game_round.player_two_choice:
            return GameOutcome(result=GameResult.TIE, winning_move=None)

        # Check if player one wins
        move_tuple = (game_round.player_one_choice, game_round.player_two_choice)
        if move_tuple in cls._WINNING_MOVES:
            return GameOutcome(
                result=GameResult.WIN,
                winning_move=cls._WINNING_MOVES[move_tuple]
            )

        # If not a draw and player one didn't win, player two must win
        # Get the winning move description by reversing the players' moves
        reverse_move = (game_round.player_two_choice, game_round.player_one_choice)
        return GameOutcome(
            result=GameResult.LOSE,
            winning_move=cls._WINNING_MOVES[reverse_move]
        ) 