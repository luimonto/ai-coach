from sqlalchemy.orm import Session

from app.repositories.activity_repository import ActivityRepository
from app.repositories.athlete_repository import AthleteRepository
from app.schemas.activity_sync import ActivitySyncItem, ActivitySyncResponse


class ActivitySyncService:
    RETENTION_LIMIT = 20

    def __init__(
        self,
        athlete_repository: AthleteRepository,
        activity_repository: ActivityRepository,
        db: Session,
    ):
        self.athlete_repository = athlete_repository
        self.activity_repository = activity_repository
        self.db = db

    def sync(
        self,
        external_id: str,
        activities: list[ActivitySyncItem],
    ) -> ActivitySyncResponse:
        athlete = self.athlete_repository.get_or_create(external_id)
        activity_data = [activity.model_dump() for activity in activities]

        try:
            created, updated, removed = self.activity_repository.upsert_and_prune(
                athlete_id=athlete.id,
                activities=activity_data,
                retention_limit=self.RETENTION_LIMIT,
            )
        except Exception:
            self.db.rollback()
            raise

        return ActivitySyncResponse(
            created=created,
            updated=updated,
            removed=removed,
            retained=len(
                self.activity_repository.get_recent_by_athlete(
                    athlete_id=athlete.id,
                    limit=self.RETENTION_LIMIT,
                )
            ),
        )
