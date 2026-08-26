from fastapi import APIRouter, Depends

from app.core.dependencies import get_workout_service
from app.schemas.coach import TrainingPlanRequest
from app.schemas.training_plan import TrainingPlanSchema
from app.services.workout_service import WorkoutService


router = APIRouter(
    prefix="/coach",
    tags=["AI Coach"],
)


@router.post(
    "/plan",
    response_model=TrainingPlanSchema,
)
def generate_training_plan(
    request: TrainingPlanRequest,
    service: WorkoutService = Depends(
        get_workout_service
    ),
) -> TrainingPlanSchema:
    return service.generate_training_roadmap(
        user_goal=request.goal
    )