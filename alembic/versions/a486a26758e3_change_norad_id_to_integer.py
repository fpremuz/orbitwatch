"""change norad_id to integer"""

from alembic import op
import sqlalchemy as sa

# IMPORTANT: pick the other head as parent
revision = "a486a26758e3"
down_revision = "f43242d5663f"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "satellites",
        "norad_id",
        type_=sa.Integer(),
        postgresql_using="norad_id::integer",
    )


def downgrade():
    op.alter_column(
        "satellites",
        "norad_id",
        type_=sa.String(),
    )