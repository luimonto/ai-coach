from fastapi import APIRouter

from app.api.v1 import ai_coach
from app.api.v1 import health
from app.api.v1 import athlete
from app.api.v1 import activities


router = APIRouter(prefix="/api/v1")

router.include_router(
    health.router
)

router.include_router(
    ai_coach.router
)

router.include_router(
    athlete.router
)

router.include_router(activities.router)
