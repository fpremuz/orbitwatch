"""add alert lifecycle

Revision ID: 2e8ed9e81dbd
Revises: b8f03dd71ae3
Create Date: 2026-05-28 00:12:22.597995
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e8ed9e81dbd"
down_revision: Union[str, Sequence[str], None] = "b8f03dd71ae3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add as nullable first
    op.add_column(
        "alerts",
        sa.Column(
            "status",
            sa.String(),
            nullable=True,
        ),
    )

    op.add_column(
        "alerts",
        sa.Column(
            "resolved_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # Populate existing rows
    op.execute(
        "UPDATE alerts SET status = 'ACTIVE'"
    )

    # Then enforce NOT NULL
    op.alter_column(
        "alerts",
        "status",
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "alerts",
        "resolved_at",
    )

    op.drop_column(
        "alerts",
        "status",
    )