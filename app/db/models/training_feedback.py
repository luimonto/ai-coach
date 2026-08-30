
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TrainingFeedback(Base):
    __tablename__ = "training_feedback"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    athlete_id: Mapped[int] = mapped_column(
        ForeignKey("athletes.id"),
        nullable=False,
        index=True,
    )

    training_plan_id: Mapped[int] = mapped_column(
        ForeignKey("training_plans.id"),
        nullable=False,
        index=True,
    )

    week_id: Mapped[int | None] = mapped_column(
        ForeignKey("training_plan_weeks.id"),
        nullable=True,
    )

    workout_id: Mapped[int | None] = mapped_column(
        ForeignKey("planned_workouts.id"),
        nullable=True,
    )

    feedback: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    athlete = relationship("Athlete")

    training_plan = relationship("TrainingPlan")

    week = relationship("TrainingPlanWeek")

    workout = relationship("PlannedWorkout")