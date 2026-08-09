from fastapi import Depends
from openai import OpenAI
from garminconnect import Garmin

from app.clients.garmin_client import get_garmin_client
from app.clients.openai_client import get_openai_client
from app.services.ai_service import AIService
from app.services.garmin_service import GarminService
from app.services.workout_service import WorkoutService


def get_ai_service(
    client: OpenAI = Depends(get_openai_client),
) -> AIService:
    return AIService(client)


def get_garmin_service(
    client: Garmin = Depends(get_garmin_client),
) -> GarminService:
    return GarminService(client)


def get_workout_service(
    ai_service: AIService = Depends(get_ai_service),
    garmin_service: GarminService = Depends(
        get_garmin_service
    ),
) -> WorkoutService:
    return WorkoutService(
        ai_service=ai_service,
        garmin_service=garmin_service,
    )