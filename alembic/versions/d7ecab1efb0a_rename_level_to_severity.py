"""rename level to severity

Revision ID: d7ecab1efb0a
Revises: fd8539a9f77d
Create Date: 2026-05-24 01:28:39.414090
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd7ecab1efb0a'
down_revision: Union[str, Sequence[str], None] = 'fd8539a9f77d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.alter_column(
        "alerts",
        "level",
        new_column_name="severity"
    )


def downgrade() -> None:

    op.alter_column(
        "alerts",
        "severity",
        new_column_name="level"
    )