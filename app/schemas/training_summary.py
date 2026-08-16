from pydantic import BaseModel, Field


class SportSummary(BaseModel):
    sport_type: str
    sessions: int = 0
    total_duration_seconds: float = 0
    total_distance_meters: float = 0
    average_heart_rate: float | None = None
    max_heart_rate: float | None = None


class TrainingSummary(BaseModel):
    period_days: int
    total_sessions: int = 0
    total_duration_seconds: float = 0
    total_distance_meters: float = 0
    sports: list[SportSummary] = Field(default_factory=list)
    recent_activities: list = Field(default_factory=list)