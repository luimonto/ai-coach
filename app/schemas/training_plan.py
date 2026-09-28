from datetime import date

from pydantic import BaseModel, Field


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



class PlannedWorkoutResponse(BaseModel):
    id: int
    scheduled_date: date
    workout_type: str
    workout_name: str
    workout_data: dict
    status: str
    garmin_workout_id: int | None = None


class CurrentWeekWorkoutsResponse(BaseModel):
    training_plan_id: int
    week_id: int
    week_number: int
    start_date: date
    end_date: date
    objective: str
    focus: list[str]
    intensity: str
    status: str
    workouts: list[PlannedWorkoutResponse]
