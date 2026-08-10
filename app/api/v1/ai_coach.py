from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_ai_service,
    get_athlete_service,
    get_workout_service,
)
from app.schemas.coach import CoachRequest, TrainingSchedule
from app.services.ai_service import AIService
from app.services.athlete_service import AthleteService
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
    ai_service: AIService = Depends(get_ai_service),
    athlete_service: AthleteService = Depends(
        get_athlete_service
    ),
    workout_service: WorkoutService = Depends(
        get_workout_service
    ),
):
    recent_workouts = workout_service.get_recent_workouts(
        limit=20
    )

    athlete_context = athlete_service.build_context(
        recent_workouts=recent_workouts
    )

    return ai_service.generate_schedule(
        athlete_context=athlete_context,
        user_goal=request.goal,
    )