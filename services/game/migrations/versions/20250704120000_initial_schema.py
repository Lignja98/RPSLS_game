"""Initial schema – create game table.

Revision ID: 20250704120000
Revises:
Create Date: 2025-07-04 12:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20250704120000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:  # noqa: D401 – imperative mood
    """Apply the migration."""

    op.create_table(
        "game",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "player_choice",
            sa.Enum("ROCK", "PAPER", "SCISSORS", "LIZARD", "SPOCK", name="choice"),
            nullable=False,
        ),
        sa.Column(
            "computer_choice",
            sa.Enum("ROCK", "PAPER", "SCISSORS", "LIZARD", "SPOCK", name="choice"),
            nullable=False,
        ),
        sa.Column(
            "winner",
            sa.Enum("player", "computer", "tie", name="gameresult"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk__game"),
    )


def downgrade() -> None:  # noqa: D401 – imperative mood
    """Rollback the migration."""

    op.drop_table("game")
