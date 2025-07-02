"""
Shared data models for the RPSLS game microservices.
"""

from enum import Enum

from pydantic import BaseModel, Field


class Choice(str, Enum):
    """Game choices enum."""

    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"
    LIZARD = "lizard"
    SPOCK = "spock"


class GameResult(str, Enum):
    """Game result enum."""

    WIN = "win"
    LOSE = "lose"
    TIE = "tie"


class ChoiceResponse(BaseModel):
    """Response model for a game choice."""

    id: int = Field(..., ge=1, le=5, description="Choice ID (1-5)")
    name: Choice = Field(..., description="Choice name")


class PlayRequest(BaseModel):
    """Request model for playing a game."""

    player: int = Field(..., ge=1, le=5, description="Player's choice ID (1-5)")


class PlayResponse(BaseModel):
    """Response model for a game result."""

    results: GameResult = Field(..., description="Game result")
    player: int = Field(..., ge=1, le=5, description="Player's choice ID")
    computer: int = Field(..., ge=1, le=5, description="Computer's choice ID")


class RandomNumberResponse(BaseModel):
    """Response model for random number API."""

    random_number: int = Field(
        ..., ge=1, le=100, description="Random number between 1-100"
    )


class PlayerCreate(BaseModel):
    """Model for creating a new player."""

    name: str = Field(..., min_length=1, max_length=100, description="Player name")


class Player(BaseModel):
    """Player model."""

    id: int = Field(..., description="Player ID")
    name: str = Field(..., description="Player name")
    wins: int = Field(default=0, description="Number of wins")
    losses: int = Field(default=0, description="Number of losses")
    ties: int = Field(default=0, description="Number of ties")
    created_at: str | None = Field(None, description="Creation timestamp")


class GameHistoryEntry(BaseModel):
    """Game history entry model."""

    id: int = Field(..., description="Game ID")
    player_id: int = Field(..., description="Player ID")
    player_choice: int = Field(..., ge=1, le=5, description="Player's choice ID")
    computer_choice: int = Field(..., ge=1, le=5, description="Computer's choice ID")
    result: GameResult = Field(..., description="Game result")
    played_at: str = Field(..., description="Game timestamp")
