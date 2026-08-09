from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_workout_service
from app.schemas.workout_request import WorkoutRequest
from app.schemas.workout_response import WorkoutResponse
from app.services.workout_service import WorkoutService
from app.schemas.workout_summary import WorkoutSummary

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
)

@router.get(
    "/workouts",
    response_model=list[WorkoutSummary],
)
def get_current_workouts(
    service: WorkoutService = Depends(get_workout_service),
):
    return service.get_current_workouts()


@router.post(
    "",
    response_model=WorkoutResponse,
)
def create_workout(
    request: WorkoutRequest,
    service: WorkoutService = Depends(
        get_workout_service
    ),
) -> WorkoutResponse:

    try:

        schedule = service.create_schedule(
            user_goal=request.goal
        )
        return WorkoutResponse(
            message="Workout schedule synchronized successfully.",
            schedule=schedule,
        )
    except ValueError as error:
        if str(error) == "unsupported_topic":
            raise HTTPException(
                status_code=400,
                detail="The AI Coach only supports fitness and workout planning.",
            )
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )