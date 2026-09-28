from datetime import date

from pydantic import BaseModel, Field
from app.schemas.activity_summary import ActivitySummary
from app.schemas.athlete import AthleteProfile
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

class AthleteContext(BaseModel):
    profile: AthleteProfile
    goals: list[str] = Field(default_factory=list)
    recent_activities: list[ActivitySummary] = Field(default_factory=list)
    upcoming_events: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    training_summary: TrainingSummary | None = None


class WorkoutDetailRequest(BaseModel):
    external_id: str = Field(
        min_length=1,
        max_length=255
    )
    week_number: int = Field(
        ge=1,
        description="The week number for which to generate the workout detail."
    )
    scheduled_date: date
