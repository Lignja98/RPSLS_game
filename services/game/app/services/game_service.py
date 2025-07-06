"""Service layer handling game logic (to be implemented)."""

from __future__ import annotations

from app.models.game import Game
from app.repositories.game_repository import GameRepository
from app.utils.enums import Choice, Mode
from app.utils.game_logic import decide_winner, random_choice
from app.utils import ai as ai_utils
from app.core.metrics import AI_MODE_TOTAL, AI_OUTCOME_TOTAL
import structlog


class GameService:  # noqa: D101 – business-logic façade
    def __init__(self, repository: GameRepository) -> None:
        self._repo = repository

    async def play(self, player_choice: Choice, mode: Mode = Mode.RANDOM) -> Game:  # noqa: D401 – imperative mood
        """Execute a game round.

        1. Pick a random choice for the computer.
        2. Decide the winner.
        3. Persist and return the *Game* entity.
        """

        log = structlog.get_logger(__name__)

        if mode is Mode.SMART:
            # Fetch recent history to feed the adaptive AI (bounded for perf)
            recent_games = await self._repo.list_recent(limit=50)
            history = [g.player_choice for g in recent_games]
            computer_choice = ai_utils.smart_choice(history)
        else:
            computer_choice = await random_choice()
        winner = decide_winner(player_choice, computer_choice)

        # Metrics
        AI_MODE_TOTAL.labels(mode=mode.value).inc()
        AI_OUTCOME_TOTAL.labels(mode=mode.value, outcome=winner.value).inc()

        # Structured log
        log.info(
            "round_played",
            mode=mode.value,
            player_choice=player_choice.name.lower(),
            computer_choice=computer_choice.name.lower(),
            outcome=winner.value,
        )

        return await self._repo.add(player_choice, computer_choice, winner)
