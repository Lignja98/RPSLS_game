"""SQLAlchemy model for a played game (to be implemented)."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.utils.enums import Choice, GameResult


class Game(Base):
    """Persisted representation of a single Rock-Paper-Scissors-Lizard-Spock game."""

    __tablename__ = "game"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – game identifier",
    )
    player_choice: Mapped[Choice] = mapped_column(
        Enum(Choice),
        nullable=False,
        comment="Player's chosen gesture",
    )
    computer_choice: Mapped[Choice] = mapped_column(
        Enum(Choice),
        nullable=False,
        comment="Computer's chosen gesture",
    )
    winner: Mapped[GameResult] = mapped_column(
        Enum(GameResult),
        nullable=False,
        comment="Outcome of the game",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="UTC timestamp when the game was played",
    )

    def __repr__(self) -> str:  # noqa: D401 – SQLA models benefit from rich repr
        return (
            f"<Game id={self.id} winner={self.winner} "
            f"player={self.player_choice} computer={self.computer_choice}>"
        ) 