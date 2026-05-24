"""add satellite health fields

Revision ID: b8f03dd71ae3
Revises: d7ecab1efb0a
Create Date: 2026-05-24 02:28:16.270127
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "b8f03dd71ae3"
down_revision: Union[str, Sequence[str], None] = "d7ecab1efb0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "satellites",
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "satellites",
        sa.Column(
            "health_score",
            sa.Float(),
            nullable=False,
            server_default="100",
        ),
    )

    # optional but cleaner:
    op.alter_column(
        "satellites",
        "health_score",
        server_default=None,
    )


def downgrade() -> None:

    op.drop_column("satellites", "health_score")

    op.drop_column("satellites", "last_seen_at")