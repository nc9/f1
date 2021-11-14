# pylint: disable=no-member
"""
acronym is optional for drivers

Revision ID: 4c0a00d4ddbe
Revises: eb4faca60b62
Create Date: 2021-11-13 17:23:03.191406

"""
import sqlalchemy as sa
from alembic import op

revision = "4c0a00d4ddbe"
down_revision = "eb4faca60b62"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("drivers", "acronym", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    op.alter_column("drivers", "acronym", existing_type=sa.VARCHAR(), nullable=False)
