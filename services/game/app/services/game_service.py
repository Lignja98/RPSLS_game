"""Service layer handling game logic (to be implemented)."""

from __future__ import annotations

from app.repositories.game_repository import GameRepository
from app.utils.enums import Choice
from app.utils.game_logic import decide_winner, random_choice
from app.models.game import Game


class GameService:  # noqa: D101 – business-logic façade
    def __init__(self, repository: GameRepository) -> None:
        self._repo = repository

    async def play(self, player_choice: Choice) -> Game:  # noqa: D401 – imperative mood
        """Execute a game round.

        1. Pick a random choice for the computer.
        2. Decide the winner.
        3. Persist and return the *Game* entity.
        """

        computer_choice = await random_choice()
        winner = decide_winner(player_choice, computer_choice)
        return await self._repo.add(player_choice, computer_choice, winner)
