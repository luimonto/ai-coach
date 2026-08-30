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


class WorkoutExercise(BaseModel):
    name: str
    description: str | None = None
    sets: int | None = None
    reps: int | None = None
    duration_seconds: int | None = None
    distance_meters: float | None = None
    intensity: str | None = None


class WorkoutDetail(BaseModel):
    workout_name: str
    workout_type: str
    objective: str
    estimated_duration_seconds: int
    exercises: list[WorkoutExercise]


class CurrentWeekResponse(BaseModel):
    training_plan_id: int
    week_id: int
    week_number: int
    start_date: date
    end_date: date
    objective: str
    focus: list[str]
    intensity: str
    status: str