from datetime import date

from pydantic import BaseModel, Field


class PlannedWorkout(BaseModel):
    week: int = Field(ge=1)
    date: date
    workout_type: str
    objective: str
    focus: str
    duration_minutes: int | None = None


class WeeklyPlan(BaseModel):
    week: int = Field(ge=1)
    objective: str
    focus: list[str]
    intensity: str


class TrainingPlanSchema(BaseModel):
    duration_weeks: int = Field(ge=1)
    overall_objective: str
    weeks: list[WeeklyPlan]