from pydantic import BaseModel


class WorkoutStep(BaseModel):
    order: int
    type: str
    description: str
    duration_seconds: int | None = None
    repetitions: int | None = None
    target: str | None = None


class WorkoutDetail(BaseModel):
    workout_name: str
    description: str | None = None
    workout_type: str
    steps: list[WorkoutStep]