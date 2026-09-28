"""scope activity identifiers to athletes

Revision ID: 41b3f1e0b7d2
Revises: 4e81c60b6c89
Create Date: 2026-09-07 12:00:00.000000
"""

from typing import Sequence, Union

from alembic import op


revision: str = "41b3f1e0b7d2"
down_revision: Union[str, Sequence[str], None] = "4e81c60b6c89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_activities_garmin_activity_id", table_name="activities")
    op.create_index(
        "ix_activities_garmin_activity_id",
        "activities",
        ["garmin_activity_id"],
        unique=False,
    )
    op.create_unique_constraint(
        "uq_activities_athlete_garmin_activity",
        "activities",
        ["athlete_id", "garmin_activity_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_activities_athlete_garmin_activity",
        "activities",
        type_="unique",
    )
    op.drop_index("ix_activities_garmin_activity_id", table_name="activities")
    op.create_index(
        "ix_activities_garmin_activity_id",
        "activities",
        ["garmin_activity_id"],
        unique=True,
    )
