from fastapi import APIRouter, Depends

from app.core.dependencies import get_ai_service
from app.schemas.coach import CoachRequest, TrainingSchedule
from app.services.ai_service import AIService


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
    service: AIService = Depends(get_ai_service),
):
    return service.generate_schedule(request.goal)