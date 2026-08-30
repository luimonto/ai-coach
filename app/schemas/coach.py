from pydantic import BaseModel, Field
from datetime import date

from app.schemas.activity_summary import ActivitySummary
from app.schemas.athlete import AthleteHistoryEntry, AthleteProfile
from app.schemas.training_plan import TrainingPlanSchema, WeeklyPlan
from app.schemas.training_summary import TrainingSummary

class TrainingPlanRequest(BaseModel):
    external_id: str = Field(
        min_length=1,
        max_length=255
    )
    goal: str = Field(
        min_length=3,
        max_length=2000,
    )

class TrainingPlanResponse(BaseModel):
    plan: TrainingPlanSchema


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
    recent_activities: list[ActivitySummary] = Field(default_factory=list)
    history: list[AthleteHistoryEntry] = Field(default_factory=list)
    upcoming_events: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    training_summary: TrainingSummary | None = None


class WorkoutDetailRequest(BaseModel):
    roadmap_week: WeeklyPlan
