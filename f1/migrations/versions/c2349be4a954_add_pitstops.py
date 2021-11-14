# pylint: disable=no-member
"""
add pitstops

Revision ID: c2349be4a954
Revises: f64fa8d2dc82
Create Date: 2021-11-14 05:10:08.952277

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "c2349be4a954"
down_revision = "f64fa8d2dc82"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pitstops",
        sa.Column("race_id", sa.Integer(), nullable=False),
        sa.Column("driver_id", sa.Integer(), nullable=False),
        sa.Column("stop", sa.Integer(), nullable=False),
        sa.Column("lap", sa.Integer(), nullable=False),
        sa.Column("time", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["driver_id"],
            ["drivers.id"],
        ),
        sa.ForeignKeyConstraint(
            ["race_id"],
            ["races.id"],
        ),
        sa.PrimaryKeyConstraint("race_id", "driver_id", "stop"),
    )
    op.create_index(op.f("ix_pitstops_driver_id"), "pitstops", ["driver_id"], unique=False)
    op.create_index(op.f("ix_pitstops_lap"), "pitstops", ["lap"], unique=False)
    op.create_index(op.f("ix_pitstops_race_id"), "pitstops", ["race_id"], unique=False)
    op.create_index(op.f("ix_pitstops_stop"), "pitstops", ["stop"], unique=False)
    op.create_index(op.f("ix_pitstops_time"), "pitstops", ["time"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_pitstops_time"), table_name="pitstops")
    op.drop_index(op.f("ix_pitstops_stop"), table_name="pitstops")
    op.drop_index(op.f("ix_pitstops_race_id"), table_name="pitstops")
    op.drop_index(op.f("ix_pitstops_lap"), table_name="pitstops")
    op.drop_index(op.f("ix_pitstops_driver_id"), table_name="pitstops")
    op.drop_table("pitstops")
    # ### end Alembic commands ###
