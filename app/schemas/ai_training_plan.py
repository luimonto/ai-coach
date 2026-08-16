from datetime import date
from pydantic import BaseModel, Field


class AIWorkout(BaseModel):
    date: date
    sport: str
    workout_type: str
    duration_minutes: int = Field(gt=0)
    intensity: str
    description: str


class AITrainingWeek(BaseModel):
    week: int = Field(gt=0)
    workouts: list[AIWorkout]


class AITrainingPlan(BaseModel):
    duration_weeks: int = Field(gt=0)
    phases: list[str]
    weeks: list[AITrainingWeek]