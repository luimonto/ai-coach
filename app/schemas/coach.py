from pydantic import BaseModel
from datetime import date


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