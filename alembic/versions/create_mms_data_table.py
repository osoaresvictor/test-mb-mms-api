"""create mms_data table"""

import sqlalchemy as sa
from alembic import op

revision = "0001_create_mms_data"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "mms_data",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("pair", sa.String, index=True),
        sa.Column("timestamp", sa.Integer, index=True),
        sa.Column("mms_20", sa.Float),
        sa.Column("mms_50", sa.Float),
        sa.Column("mms_200", sa.Float),
    )


def downgrade():
    op.drop_table("mms_data")
