from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TrainingPlanWeek(Base):
    __tablename__ = "training_plan_weeks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    training_plan_id: Mapped[int] = mapped_column(
        ForeignKey("training_plans.id"),
        nullable=False,
        index=True,
    )

    week_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    objective: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    focus: Mapped[list] = mapped_column(
        # PostgreSQL JSON
        JSON,
        nullable=False,
    )

    intensity: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    training_plan = relationship(
        "TrainingPlan",
        back_populates="weeks",
    )

    workouts = relationship(
        "PlannedWorkout",
        back_populates="week",
        cascade="all, delete-orphan",
    )