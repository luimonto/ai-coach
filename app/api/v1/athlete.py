from fastapi import APIRouter, Depends

from app.schemas.athlete import AthleteProfile
from app.services.athlete_service import AthleteService


router = APIRouter(
    prefix="/athlete",
    tags=["athlete"],
)

athlete_service = AthleteService()


def get_athlete_service() -> AthleteService:
    return athlete_service


@router.get("", response_model=AthleteProfile)
def get_athlete(
    service: AthleteService = Depends(get_athlete_service),
) -> AthleteProfile:
    return service.get_profile()


@router.put("", response_model=AthleteProfile)
def update_athlete(
    profile: AthleteProfile,
    service: AthleteService = Depends(get_athlete_service),
) -> AthleteProfile:
    return service.update_profile(profile)