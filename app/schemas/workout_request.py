from pydantic_settings import BaseSettings


class WorkoutRequest(BaseSettings):
    """Workout request schema."""
    goal: str
    athlete_level: str
    available_days: int