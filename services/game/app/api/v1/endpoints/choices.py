from __future__ import annotations

"""Choice-related endpoints."""

from fastapi import APIRouter

from app.schemas.game import ChoiceRead
from app.utils.enums import Choice
from app.utils.game_logic import random_choice

router = APIRouter()


@router.get(
    "/choices", response_model=list[ChoiceRead], summary="List available choices"
)
async def list_choices() -> list[ChoiceRead]:
    """Return all playable gestures (static)."""

    return [ChoiceRead.from_enum(c) for c in Choice]


@router.get("/choice", response_model=ChoiceRead, summary="Get a random choice")
async def get_random_choice() -> ChoiceRead:
    """Return a server-generated random choice (used by the UI)."""

    choice = await random_choice()
    return ChoiceRead.from_enum(choice)
