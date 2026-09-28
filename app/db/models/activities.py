from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint(
            "athlete_id",
            "garmin_activity_id",
            name="uq_activities_athlete_garmin_activity",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    athlete_id: Mapped[int] = mapped_column(
        ForeignKey("athletes.id"),
        nullable=False,
        index=True,
    )

    garmin_activity_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
    )

    activity_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sport_type_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    distance_meters: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    average_heart_rate: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    max_heart_rate: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    calories: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
