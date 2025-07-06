from __future__ import annotations

import pytest

from app.utils.ai import smart_choice
from app.utils.enums import Choice


@pytest.mark.parametrize(
    "history,expected_counters",
    [
        ([Choice.ROCK] * 4, {Choice.PAPER, Choice.SPOCK}),
        (
            [Choice.SCISSORS, Choice.SCISSORS, Choice.SCISSORS],
            {Choice.ROCK, Choice.SPOCK},
        ),
        ([Choice.LIZARD] * 10, {Choice.ROCK, Choice.SCISSORS}),
    ],
)
def test_smart_choice_counter(history, expected_counters, monkeypatch):
    """smart_choice should return a gesture that beats the player's frequent move."""

    import app.utils.ai as ai_mod

    monkeypatch.setattr(ai_mod, "rand_choice", lambda seq: seq[0], raising=True)

    choice = smart_choice(history)

    assert choice in expected_counters


def test_smart_choice_empty_history(monkeypatch):
    """With no history the function returns *any* valid gesture."""

    import app.utils.ai as ai_mod

    monkeypatch.setattr(ai_mod, "rand_choice", lambda seq: seq[0], raising=True)
    result = smart_choice([])
    assert isinstance(result, Choice)
