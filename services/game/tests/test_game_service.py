import app.services.game_service as gs
from app.services.game_service import GameService
from app.utils import game_logic as gl
from app.utils.enums import Choice
import pytest


class DummyRepository:
    """Minimal stub mirroring *GameRepository*'s public surface."""

    def __init__(self):
        self.add_calls: list[tuple] = []

    async def add(self, player_choice, computer_choice, winner):  # noqa: D401 – mimic repo
        self.add_calls.append((player_choice, computer_choice, winner))
        return object()  # sentinel value to verify passthrough


@pytest.mark.asyncio
async def test_play_uses_random_choice_and_repo(monkeypatch):
    """*GameService.play* should orchestrate the round and persist via repository."""

    sentinel = object()

    class SentinelRepo(DummyRepository):
        async def add(self, player_choice, computer_choice, winner):
            self.add_calls.append((player_choice, computer_choice, winner))
            return sentinel

    dummy_repo = SentinelRepo()
    service = GameService(dummy_repo)  # type: ignore[arg-type]

    # Force deterministic computer move
    async def fake_random_choice():
        return Choice.LIZARD

    # Patch the symbol that *GameService* closed over at import time
    monkeypatch.setattr(gs, "random_choice", fake_random_choice, raising=True)

    player_move = Choice.SPOCK
    result = await service.play(player_move)

    # Repository should be invoked exactly once with correct arguments
    assert len(dummy_repo.add_calls) == 1
    recorded_player, recorded_computer, recorded_winner = dummy_repo.add_calls[0]

    assert recorded_player is player_move
    assert recorded_computer is Choice.LIZARD
    assert recorded_winner is gl.decide_winner(player_move, Choice.LIZARD)

    # Service should return whatever the repository returns (sentinel object)
    assert result is sentinel
