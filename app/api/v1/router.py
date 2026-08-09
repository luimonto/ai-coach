from fastapi import APIRouter

from app.api.v1 import ai_coach
from app.api.v1 import health
from app.api.v1 import workout
from app.api.v1 import athlete


router = APIRouter(prefix="/api/v1")

router.include_router(
    health.router,
)

router.include_router(
    workout.router,
)

router.include_router(
    ai_coach.router,
)

router.include_router(
    athlete.router,
)