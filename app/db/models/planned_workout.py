from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class PlannedWorkout(Base):
    __tablename__ = "planned_workouts"

    __table_args__ = (
        UniqueConstraint(
            "week_id",
            "scheduled_date",
            name="uq_planned_workout_week_date",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    week_id: Mapped[int] = mapped_column(
        ForeignKey("training_plan_weeks.id"),
        nullable=False,
        index=True,
    )

    scheduled_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    workout_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    workout_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    workout_data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="planned",
        index=True,
    )

    garmin_workout_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    week = relationship(
        "TrainingPlanWeek",
        back_populates="workouts",
    )