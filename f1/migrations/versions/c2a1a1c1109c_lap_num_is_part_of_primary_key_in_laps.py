# pylint: disable=no-member
"""
lap num is part of primary key in laps

Revision ID: c2a1a1c1109c
Revises: c2349be4a954
Create Date: 2021-11-14 15:27:42.756010

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c2a1a1c1109c"
down_revision = "c2349be4a954"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("alter table laps drop constraint laps_pkey;")
    op.execute("alter table laps add constraint laps_pkey primary key (race_id, driver_id, lap);")


def downgrade() -> None:
    pass
