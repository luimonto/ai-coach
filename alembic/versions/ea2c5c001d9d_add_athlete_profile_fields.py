"""add athlete profile fields

Revision ID: ea2c5c001d9d
Revises: 41b3f1e0b7d2
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "ea2c5c001d9d"
down_revision: Union[str, Sequence[str], None] = "41b3f1e0b7d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("athletes", sa.Column("name", sa.String(length=120), nullable=True))
    op.add_column("athletes", sa.Column("age", sa.Integer(), nullable=True))
    op.add_column("athletes", sa.Column("height_cm", sa.Float(), nullable=True))
    op.add_column("athletes", sa.Column("weight_kg", sa.Float(), nullable=True))
    op.add_column("athletes", sa.Column("experience_level", sa.String(length=50), nullable=True))
    op.add_column("athletes", sa.Column("primary_sport", sa.String(length=50), nullable=True))
    op.add_column("athletes", sa.Column("secondary_sports", sa.JSON(), nullable=True))
    op.add_column("athletes", sa.Column("weekly_training_days", sa.Integer(), nullable=True))
    op.add_column("athletes", sa.Column("preferred_training_days", sa.JSON(), nullable=True))
    op.add_column("athletes", sa.Column("goals", sa.JSON(), nullable=True))
    op.add_column("athletes", sa.Column("notes", sa.Text(), nullable=True))
    op.execute("UPDATE athletes SET secondary_sports = '[]', preferred_training_days = '[]', goals = '[]'")
    op.alter_column("athletes", "secondary_sports", nullable=False)
    op.alter_column("athletes", "preferred_training_days", nullable=False)
    op.alter_column("athletes", "goals", nullable=False)


def downgrade() -> None:
    for column in (
        "notes", "goals", "preferred_training_days", "weekly_training_days",
        "secondary_sports", "primary_sport", "experience_level", "weight_kg",
        "height_cm", "age", "name",
    ):
        op.drop_column("athletes", column)
