from __future__ import annotations

"""Adaptive computer strategy helpers."""

from collections import Counter
from random import choice as rand_choice
from collections.abc import Sequence

from app.utils.enums import Choice

__all__ = [
    "smart_choice",
]


# Mapping of player gesture -> set of gestures that beat it (reuse from game_logic)
_BEATS: dict[Choice, set[Choice]] = {
    Choice.ROCK: {Choice.PAPER, Choice.SPOCK},
    Choice.PAPER: {Choice.SCISSORS, Choice.LIZARD},
    Choice.SCISSORS: {Choice.ROCK, Choice.SPOCK},
    Choice.LIZARD: {Choice.ROCK, Choice.SCISSORS},
    Choice.SPOCK: {Choice.PAPER, Choice.LIZARD},
}


def smart_choice(history: Sequence[Choice], *, window: int = 5) -> Choice:
    """Return an adaptive computer move based on player's recent history.

    Strategy:
    1. Consider the last *window* moves (defaults to 5).
    2. Find the player's most frequent gesture.
    3. Pick **randomly** among the gestures that beat that frequent choice.

    If the *history* is empty or no winner can be derived, a random gesture is
    returned (uniform over the 5 choices).
    """

    if not history:
        return rand_choice(list(Choice))

    # History is expected to be ordered from newest -> oldest.
    # We want the *recent* window, i.e. the first *window* items.
    window_history = history[:window]
    counts = Counter(window_history)
    # Most common returns list of (choice, count) sorted desc
    most_common_choice, _ = counts.most_common(1)[0]

    counters = _BEATS[most_common_choice]
    return rand_choice(list(counters))
