"""Enum definitions for game choices and outcomes."""

from enum import IntEnum, StrEnum


class Choice(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIZARD = 4
    SPOCK = 5


class GameResult(StrEnum):
    PLAYER = "player"
    COMPUTER = "computer"
    TIE = "tie"


class Mode(StrEnum):
    """Available computer strategies for a round."""

    RANDOM = "random"
    SMART = "smart"
