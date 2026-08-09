from datetime import datetime
from typing import Any
from pydantic import BaseModel

class WorkoutSummary(BaseModel):
    """Workout summary schema."""
    workout_id: int
    workout_name: str
    sport_type_id: int
    sport_type_key: str
    description: str | None = None
    estimated_duration_seconds: int | None = None
    estimated_distance_meters: float | None = None
    created_date: datetime | None = None
    update_date: datetime | None = None