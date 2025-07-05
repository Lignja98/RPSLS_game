import pytest

from app.utils.enums import Choice, GameResult
from app.utils import game_logic as gl


@pytest.mark.parametrize(
    "player,computer,expected",
    [
        (Choice.ROCK, Choice.ROCK, GameResult.TIE),
        (Choice.ROCK, Choice.SCISSORS, GameResult.PLAYER),
        (Choice.SCISSORS, Choice.ROCK, GameResult.COMPUTER),
    ],
)
def test_decide_winner_basic(player, computer, expected):
    """Ensure *decide_winner* returns the documented outcomes."""

    assert gl.decide_winner(player, computer) == expected


@pytest.mark.parametrize(
    "player,computer",
    [
        (Choice.ROCK, Choice.SCISSORS),
        (Choice.ROCK, Choice.LIZARD),
        (Choice.PAPER, Choice.ROCK),
        (Choice.PAPER, Choice.SPOCK),
        (Choice.SCISSORS, Choice.PAPER),
        (Choice.SCISSORS, Choice.LIZARD),
        (Choice.LIZARD, Choice.SPOCK),
        (Choice.LIZARD, Choice.PAPER),
        (Choice.SPOCK, Choice.SCISSORS),
        (Choice.SPOCK, Choice.ROCK),
    ],
)
def test_decide_winner_exhaustive(player, computer):
    """For every winning combination the function must be symmetric."""

    assert gl.decide_winner(player, computer) == GameResult.PLAYER
    assert gl.decide_winner(computer, player) == GameResult.COMPUTER


@pytest.mark.asyncio
async def test_random_choice_endpoint(monkeypatch):
    """*random_choice* should use the external endpoint when available."""

    # Stub ``httpx.AsyncClient`` so no real HTTP request is made
    class DummyResp:  # minimal subset used by the code under test
        def __init__(self, num: int):
            self._num = num

        def raise_for_status(self):
            pass

        def json(self):
            return {"random_number": self._num}

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, url):
            return DummyResp(42)

    monkeypatch.setattr(gl.httpx, "AsyncClient", DummyClient)

    choice = await gl.random_choice()
    expected_idx = (42 - 1) % 5
    assert choice is list(Choice)[expected_idx]


@pytest.mark.asyncio
async def test_random_choice_fallback(monkeypatch):
    """When the HTTP call fails the function must fall back to *random* module."""

    # Force the http client to raise so we hit the fallback branch
    class ErrorClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, url):
            raise gl.httpx.HTTPError("boom")

    monkeypatch.setattr(gl.httpx, "AsyncClient", ErrorClient)
    monkeypatch.setattr(gl.random, "randint", lambda a, b: 3)

    choice = await gl.random_choice()
    expected_idx = (3 - 1) % 5
    assert choice is list(Choice)[expected_idx]
