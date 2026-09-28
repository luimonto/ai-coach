from fastapi import Depends
from openai import OpenAI
from sqlalchemy.orm import Session

from app.clients.openai_client import get_openai_client
from app.services.ai_service import AIService
from app.services.athlete_service import AthleteService
from app.services.activity_sync_service import ActivitySyncService
from app.services.workout_service import WorkoutService
from app.services.training_analysis_service import TrainingAnalysisService
from app.repositories.athlete_repository import AthleteRepository
from app.repositories.training_plan_repository import TrainingPlanRepository
from app.repositories.planned_workout_repository import PlannedWorkoutRepository
from app.repositories.activity_repository import ActivityRepository
from app.db.session import get_db


def get_athlete_repository(
    db: Session = Depends(get_db),
) -> AthleteRepository:
    return AthleteRepository(db)


def get_athlete_service(
    athlete_repository: AthleteRepository = Depends(get_athlete_repository),
) -> AthleteService:
    return AthleteService(athlete_repository)


def get_ai_service(
    client: OpenAI = Depends(get_openai_client),
) -> AIService:
    return AIService(client)


def get_training_analysis_service(
) -> TrainingAnalysisService:
    return TrainingAnalysisService()


def get_activity_repository(
    db: Session = Depends(get_db),
) -> ActivityRepository:
    return ActivityRepository(db)

def get_activity_sync_service(
    db: Session = Depends(get_db),
    activity_repository: ActivityRepository = Depends(get_activity_repository),
) -> ActivitySyncService:
    athlete_repository = AthleteRepository(db)
    return ActivitySyncService(
        athlete_repository=athlete_repository,
        activity_repository=activity_repository,
        db=db,
    )


def get_workout_service(
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(
        get_ai_service
    ),
    athlete_service: AthleteService = Depends(
        get_athlete_service
    ),
    training_analysis_service: TrainingAnalysisService = Depends(
        get_training_analysis_service
    ),
    activity_repository: ActivityRepository = Depends(
        get_activity_repository
    )
) -> WorkoutService:

    athlete_repository = AthleteRepository(db)
    training_plan_repository = TrainingPlanRepository(db)
    planned_workout_repository = (
        PlannedWorkoutRepository(db)
    )
    return WorkoutService(
        db=db,
        ai_service=ai_service,
        athlete_service=athlete_service,
        training_analysis_service=training_analysis_service,
        athlete_repository=athlete_repository,
        training_plan_repository=training_plan_repository,
        planned_workout_repository=planned_workout_repository,
        activity_repository=activity_repository
    )
