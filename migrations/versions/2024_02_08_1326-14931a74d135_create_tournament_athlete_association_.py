"""Create tournament_athlete_association_table

Revision ID: 14931a74d135
Revises: 95ebac8275c8
Create Date: 2024-02-08 13:26:26.828982

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "14931a74d135"
down_revision: Union[str, None] = "95ebac8275c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tournament_athlete_associations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tournament_id", sa.Integer(), nullable=False),
        sa.Column("athlete_id", sa.Integer(), nullable=False),
        sa.Column("place", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["athlete_id"],
            ["athletes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tournament_id"],
            ["tournaments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tournament_id", "athlete_id", name="idx_unique_tournament_athlete"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tournament_athlete_associations")
    # ### end Alembic commands ###
