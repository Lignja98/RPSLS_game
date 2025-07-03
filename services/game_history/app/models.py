"""
Database and API models for the game history service.
"""

from datetime import datetime, UTC
from typing import List, Optional, Any

from sqlalchemy import Column, DateTime, Enum, Integer, String, event
from sqlalchemy.orm import DeclarativeBase, validates
from pydantic import BaseModel, Field

from shared.models import Choice, GameResult, GameHistoryEntry


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class GameHistory(Base):
    """SQLAlchemy model for game history entries."""
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, index=True, nullable=False)
    player_choice = Column(
        Enum(Choice, values_callable=lambda x: [e.value for e in x]), 
        nullable=False
    )
    computer_choice = Column(
        Enum(Choice, values_callable=lambda x: [e.value for e in x]), 
        nullable=False
    )
    result = Column(
        Enum(GameResult, values_callable=lambda x: [e.value for e in x]), 
        nullable=False
    )
    winning_move = Column(String, nullable=True)
    played_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    @validates('player_id')
    def validate_player_id(self, key: str, value: Any) -> int:
        """Validate player_id."""
        if value is None:
            raise ValueError("player_id cannot be None")
        return value

    @validates('player_choice', 'computer_choice')
    def validate_choice(self, key: str, value: Any) -> Choice:
        """Validate choice fields."""
        if not isinstance(value, Choice):
            try:
                value = Choice(value)
            except ValueError:
                raise ValueError(f"Invalid {key}: {value}")
        return value

    @validates('result')
    def validate_result(self, key: str, value: Any) -> GameResult:
        """Validate result field."""
        if not isinstance(value, GameResult):
            try:
                value = GameResult(value)
            except ValueError:
                raise ValueError(f"Invalid {key}: {value}")
        return value

    def __str__(self) -> str:
        """Return string representation of the game history entry."""
        return f"GameHistory(id={self.id}, player_id={self.player_id}, result={self.result.value})"

    def __repr__(self) -> str:
        """Return detailed string representation of the game history entry."""
        return (f"GameHistory(id={self.id}, player_id={self.player_id}, "
                f"player_choice={self.player_choice.value}, computer_choice={self.computer_choice.value}, "
                f"result={self.result.value}, winning_move={self.winning_move!r})")

    def to_response(self) -> GameHistoryEntry:
        """Convert to API response model."""
        return GameHistoryEntry(
            id=self.id,
            player_id=self.player_id,
            player_choice=self.player_choice,
            computer_choice=self.computer_choice,
            result=self.result,
            played_at=self.played_at.isoformat()
        )


class GameHistoryCreate(BaseModel):
    """Model for creating a new game history record (input DTO)."""
    player_id: int
    player_choice: Choice
    computer_choice: Choice
    result: GameResult
    winning_move: Optional[str] = None


class GameHistoryFilter(BaseModel):
    """Filtering parameters when querying game history."""
    player_id: Optional[int] = None
    result: Optional[GameResult] = None
    limit: int = Field(10, gt=0)
    offset: int = Field(0, ge=0)


class GameHistoryList(BaseModel):
    """List response for game history queries."""
    total: int
    entries: List[GameHistoryEntry] 