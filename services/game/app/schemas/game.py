from __future__ import annotations

"""Pydantic schemas exposed by the Game API layer."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.utils.enums import Choice, GameResult, Mode

__all__ = [
    "ChoiceRead",
    "PlayRequest",
    "PlayResponse",
    "GameRead",
]


# ---------------------------------------------------------------------------
# Helper mappers
# ---------------------------------------------------------------------------

_PLAYER_OUTCOME_MAP: dict[GameResult, str] = {
    GameResult.PLAYER: "win",
    GameResult.COMPUTER: "lose",
    GameResult.TIE: "tie",
}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class ChoiceRead(BaseModel):
    """Public representation of a *Choice* enum member."""

    id: int = Field(..., ge=1, le=5)
    name: str

    @classmethod
    def from_enum(cls, choice: Choice) -> ChoiceRead:
        return cls(id=choice.value, name=choice.name.lower())

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1, "name": "rock"},
                {"id": 2, "name": "paper"},
            ]
        }
    }


class PlayRequest(BaseModel):
    """Payload for POST /play."""

    player: int = Field(..., ge=1, le=5, description="Choice identifier 1-5")
    mode: Mode = Field(
        default=Mode.RANDOM,
        description="AI strategy to use (random | smart).",
    )

    @field_validator("player")
    @classmethod
    def _validate_choice(cls, v: int) -> int:
        if v not in {c.value for c in Choice}:
            raise ValueError("player must be between 1 and 5 (valid choice id)")
        return v

    def to_choice(self) -> Choice:
        """Return the *Choice* enum corresponding to the player field."""

        return Choice(self.player)


class PlayResponse(BaseModel):
    """Response returned by POST /play."""

    results: str = Field(description="win | lose | tie from the player's perspective")
    player: int
    computer: int

    @classmethod
    def from_round(
        cls,
        player_choice: Choice,
        computer_choice: Choice,
        outcome: GameResult,
    ) -> PlayResponse:
        return cls(
            results=_PLAYER_OUTCOME_MAP[outcome],
            player=player_choice.value,
            computer=computer_choice.value,
        )


class GameRead(PlayResponse):
    """Extended representation used in scoreboard endpoints."""

    id: uuid.UUID
    timestamp: datetime

    @classmethod
    def from_model(cls, game: Any) -> GameRead:
        # Deferred import to avoid circular dependency
        from app.models.game import Game

        assert isinstance(game, Game)
        return cls(
            id=game.id,
            timestamp=game.created_at,
            results=_PLAYER_OUTCOME_MAP[game.winner],
            player=game.player_choice.value,
            computer=game.computer_choice.value,
        )

    model_config = ConfigDict(from_attributes=True)
