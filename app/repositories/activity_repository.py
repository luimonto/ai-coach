from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.activities import Activity


class ActivityRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_recent_by_athlete(
        self,
        athlete_id: int,
        limit: int = 10,
        since: datetime | None = None,
    ) -> list[Activity]:
        statement = select(Activity).where(Activity.athlete_id == athlete_id)
        if since:
            statement = statement.where(Activity.start_time >= since)
        statement = statement.order_by(Activity.start_time.desc()).limit(limit)
        return list(self.db.scalars(statement))

    def upsert_and_prune(
        self,
        athlete_id: int,
        activities: Sequence[dict],
        retention_limit: int,
    ) -> tuple[int, int, int]:
        """Persist a client sync as one transaction and retain recent history."""
        activity_ids = [item["garmin_activity_id"] for item in activities]
        existing_by_garmin_id: dict[int, Activity] = {}

        if activity_ids:
            existing = self.db.scalars(
                select(Activity).where(
                    Activity.athlete_id == athlete_id,
                    Activity.garmin_activity_id.in_(activity_ids),
                )
            ).all()
            existing_by_garmin_id = {
                activity.garmin_activity_id: activity for activity in existing
            }

        created = 0
        updated = 0
        for item in activities:
            activity = existing_by_garmin_id.get(item["garmin_activity_id"])
            if activity is None:
                self.db.add(Activity(athlete_id=athlete_id, **item))
                created += 1
                continue

            for field, value in item.items():
                setattr(activity, field, value)
            updated += 1

        self.db.flush()

        stale_ids = self.db.scalars(
            select(Activity.id)
            .where(Activity.athlete_id == athlete_id)
            .order_by(Activity.start_time.desc(), Activity.id.desc())
            .offset(retention_limit)
        ).all()
        removed = len(stale_ids)
        if stale_ids:
            self.db.execute(delete(Activity).where(Activity.id.in_(stale_ids)))

        self.db.commit()
        return created, updated, removed
