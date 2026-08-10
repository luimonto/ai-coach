from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    garmin_workout_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
    )

    workout_name: Mapped[str] = mapped_column(
        String(255),
    )

    sport_type_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    sport_type_key: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    estimated_duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    estimated_distance_meters: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    synced_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )