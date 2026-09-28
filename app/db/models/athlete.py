from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Athlete(Base):
    __tablename__ = "athletes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    primary_sport: Mapped[str | None] = mapped_column(String(50), nullable=True)
    secondary_sports: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    weekly_training_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preferred_training_days: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    goals: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    training_plans = relationship(
        "TrainingPlan",
        back_populates="athlete",
        cascade="all, delete-orphan",
    )
