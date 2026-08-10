from pydantic import BaseModel, Field
from datetime import date

from app.schemas.athlete import AthleteHistoryEntry, AthleteProfile
from app.schemas.workout_summary import WorkoutSummary


class CoachRequest(BaseModel):
    """Coach request schema."""
    goal: str


class CoachResponse(BaseModel):
    """Coach response schema."""
    recommendation: str
    sport: str | None = None


class WorkoutData(BaseModel):
    date: date
    sport: str
    workout_name: str
    description: str
    duration_minutes: int | None = None
    distance_meters: float | None = None


class TrainingSchedule(BaseModel):
    workoutData: list[WorkoutData]


class AthleteContext(BaseModel):
    profile: AthleteProfile
    goals: list[str] = Field(default_factory=list)
    recent_workouts: list[WorkoutSummary] = Field(default_factory=list)
    history: list[AthleteHistoryEntry] = Field(default_factory=list)
    upcoming_events: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)