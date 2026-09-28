from fastapi import APIRouter, Depends

from app.core.dependencies import get_workout_service
from app.schemas.coach import TrainingPlanRequest, WorkoutDetailRequest
from app.schemas.training_plan import TrainingPlanSchema, WorkoutDetail, CurrentWeekWorkoutsResponse
from app.services.workout_service import WorkoutService
from app.schemas.training_plan import CurrentWeekResponse


router = APIRouter(
    prefix="/coach",
    tags=["AI Coach"],
)


@router.post("/plan", response_model=TrainingPlanSchema)
def generate_training_plan(
    request: TrainingPlanRequest,
    service: WorkoutService = Depends(
        get_workout_service
    ),
) -> TrainingPlanSchema:

    return service.generate_training_roadmap(
        external_id=request.external_id,
        user_goal=request.goal,
    )

@router.post("/plan/workout", response_model=WorkoutDetail)
def generate_workout(
    request: WorkoutDetailRequest,
    service: WorkoutService = Depends(
        get_workout_service
    ),
) -> WorkoutDetail:

    return service.generate_workout_detail(
        external_id=request.external_id,
        week_number=request.week_number,
        scheduled_date=request.scheduled_date,
    )

@router.get("/plan/current-week", response_model=CurrentWeekResponse)
def get_current_week(
    external_id: str,
    service: WorkoutService = Depends(
        get_workout_service
    ),
) -> CurrentWeekResponse:
    return service.get_current_week(
        external_id=external_id
    )

@router.get("/plan/current-week/workouts", response_model=CurrentWeekWorkoutsResponse)
def get_current_week_workouts(
    external_id: str,
    service: WorkoutService = Depends(
        get_workout_service
    ),
) -> CurrentWeekWorkoutsResponse:

    return service.get_current_week_workouts(
        external_id=external_id
    )