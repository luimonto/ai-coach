from pydantic import BaseModel, Field
from datetime import date

from app.schemas.workout_summary import WorkoutSummary


class AthleteProfile(BaseModel):
    name: str | None = None
    age: int | None = Field(default=None, ge=13, le=100)
    height_cm: float | None = Field(default=None, gt=0)
    weight_kg: float | None = Field(default=None, gt=0)

    experience_level: str | None = None

    primary_sport: str | None = None
    secondary_sports: list[str] = Field(default_factory=list)

    weekly_training_days: int | None = Field(
        default=None,
        ge=1,
        le=7,
    )

    preferred_training_days: list[str] = Field(
        default_factory=list
    )

    goals: list[str] = Field(
        default_factory=list
    )

    notes: str | None = None



class AthleteHistoryEntry(BaseModel):
    date: date
    sport: str
    event: str | None = None
    distance_meters: float | None = None
    duration_seconds: int | None = None
    notes: str | None = None


class AthleteContext(BaseModel):
    profile: AthleteProfile
    goals: list[str] = []
    recent_workouts: list[WorkoutSummary] = []
    history: list[AthleteHistoryEntry] = []
    upcoming_events: list[str] = []
    notes: list[str] = []