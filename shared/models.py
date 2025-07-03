"""
Shared data models for the RPSLS game microservices.
"""

from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field


class Choice(str, Enum):
    """Game choices enum.
    
    Example:
        >>> choice = Choice.ROCK
        >>> choice.value
        'rock'
    """
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"
    LIZARD = "lizard"
    SPOCK = "spock"


class GameResult(str, Enum):
    """Game result enum.
    
    Example:
        >>> result = GameResult.WIN
        >>> result.value
        'win'
    """
    WIN = "win"
    LOSE = "lose"
    TIE = "tie"


class ChoiceResponse(BaseModel):
    """Response model for a game choice.
    
    Example:
        >>> choice = ChoiceResponse(id=1, name=Choice.ROCK)
        >>> choice.model_dump()
        {'id': 1, 'name': 'rock'}
    """
    id: int = Field(
        ...,
        ge=1,
        le=5,
        description="Choice ID (1-5, where 1=rock, 2=paper, 3=scissors, 4=lizard, 5=spock)"
    )
    name: Choice = Field(
        ...,
        description="Choice name (rock, paper, scissors, lizard, spock)"
    )


class PlayRequest(BaseModel):
    """Request model for playing a game.
    
    Example:
        >>> request = PlayRequest(choice=Choice.ROCK)
        >>> request.model_dump()
        {'choice': 'rock'}
    """
    choice: Choice = Field(
        ...,
        description="Player's choice (rock, paper, scissors, lizard, spock)"
    )


class PlayResponse(BaseModel):
    """Response model for a game result.
    
    Example:
        >>> response = PlayResponse(
        ...     result=GameResult.WIN,
        ...     player_choice=Choice.ROCK,
        ...     computer_choice=Choice.SCISSORS,
        ...     winning_move="Rock crushes Scissors"
        ... )
    """
    result: GameResult = Field(
        ...,
        description="Game result (win/lose/tie)"
    )
    player_choice: Choice = Field(
        ...,
        description="Player's choice"
    )
    computer_choice: Choice = Field(
        ...,
        description="Computer's choice"
    )
    winning_move: str | None = Field(
        None,
        description="Description of the winning move (null for ties)"
    )


class RandomNumberResponse(BaseModel):
    """Response model for random number API."""
    random_number: int = Field(
        ...,
        ge=1,
        le=100,
        description="Random number between 1-100"
    )


class PlayerCreate(BaseModel):
    """Model for creating a new player."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Player name"
    )


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
    id: Optional[int] = None
    player_id: int
    player_choice: Choice
    computer_choice: Choice
    result: GameResult
    winning_move: Optional[str] = None
    played_at: Optional[str] = None


class PlayerStats(BaseModel):
    """Player statistics model."""
    player_id: int
    stats: Dict[str, int]  # Maps GameResult values to counts
 