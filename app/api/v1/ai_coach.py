from fastapi import APIRouter, Depends

from app.core.dependencies import get_workout_service
from app.schemas.coach import CoachRequest, TrainingSchedule
from app.services.workout_service import WorkoutService


router = APIRouter(
    prefix="/coach",
    tags=["AI Coach"],
)


@router.post(
    "/schedule",
    response_model=TrainingSchedule,
)
def generate_schedule(
    request: CoachRequest,
    service: WorkoutService = Depends(
        get_workout_service
    ),
):
    return service.generate_training_schedule(
        user_goal=request.goal
    )