from datetime import date
from pydantic import BaseModel, Field


class TrainingSession(BaseModel):
    date: date
    sport: str
    duration_minutes: int = Field(
        gt=0,
        le=300,
    )
    intensity: str
    description: str

class TrainingPlan(BaseModel):
    sessions: list[TrainingSession]