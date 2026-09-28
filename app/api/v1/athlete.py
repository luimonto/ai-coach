from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_athlete_service
from app.schemas.athlete import AthleteProfile
from app.services.athlete_service import AthleteService


router = APIRouter(
    prefix="/athlete",
    tags=["athlete"],
)


@router.get("/{external_id}", response_model=AthleteProfile)
def get_athlete_profile(
    external_id: str,
    service: AthleteService = Depends(get_athlete_service),
) -> AthleteProfile:
    profile = service.get_profile(external_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="athlete_not_found")
    return profile


@router.put("/{external_id}", response_model=AthleteProfile)
def update_athlete_profile(
    external_id: str,
    profile: AthleteProfile,
    service: AthleteService = Depends(get_athlete_service),
) -> AthleteProfile:
    return service.update_profile(external_id, profile)
