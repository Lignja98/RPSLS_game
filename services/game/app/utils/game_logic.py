from __future__ import annotations

import random

import httpx

from app.core.config import get_settings
from app.utils.enums import Choice, GameResult

__all__ = [
    "decide_winner",
    "random_choice",
]


_BEATS: dict[Choice, set[Choice]] = {
    Choice.ROCK: {Choice.SCISSORS, Choice.LIZARD},
    Choice.PAPER: {Choice.ROCK, Choice.SPOCK},
    Choice.SCISSORS: {Choice.PAPER, Choice.LIZARD},
    Choice.LIZARD: {Choice.SPOCK, Choice.PAPER},
    Choice.SPOCK: {Choice.SCISSORS, Choice.ROCK},
}


def decide_winner(player: Choice, computer: Choice) -> GameResult:  # noqa: D401 – imperative mood
    """Return the outcome of a single RPSLS round.

    Parameters
    ----------
    player, computer: Choice
        Gestures chosen by the player and the computer.

    Returns
    -------
    GameResult
        ``PLAYER`` if the player wins, ``COMPUTER`` if the computer wins,
        otherwise ``TIE``.
    """

    if player == computer:
        return GameResult.TIE

    if computer in _BEATS[player]:
        return GameResult.PLAYER

    return GameResult.COMPUTER


async def random_choice() -> Choice:  # noqa: D401 – imperative mood
    """Return a random RPSLS choice for the computer.

    Attempts to obtain a truly random integer in the range 1-100 from the
    public code-challenge endpoint and maps it deterministically to one of the
    five RPSLS gestures. If the request fails for *any* reason - network
    issues, non-2xx response, malformed JSON, etc. - the function falls back
    to Python's local PRNG so the service remains responsive.
    """

    settings = get_settings()

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(settings.RANDOM_API_URL)
            resp.raise_for_status()
            idx = int(resp.json().get("random_number", 0))
    except Exception:  # noqa: BLE001 – broad except to ensure graceful fallback
        idx = random.randint(1, 100)

    gestures = list(Choice)
    return gestures[(idx - 1) % len(gestures)]
