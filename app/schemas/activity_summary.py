from datetime import datetime

from pydantic import BaseModel


class ActivitySummary(BaseModel):
    activity_id: int
    activity_name: str

    sport_type_key: str

    start_time: datetime | None = None

    duration_seconds: float | None = None
    distance_meters: float | None = None

    average_heart_rate: float | None = None
    max_heart_rate: float | None = None

    calories: float | None = None