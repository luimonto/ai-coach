from datetime import date
from sqlalchemy.orm import Session
from app.db.models.planned_workout import PlannedWorkout


class PlannedWorkoutRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_week_and_date(
        self,
        week_id: int,
        scheduled_date: date,
    ) -> PlannedWorkout | None:

        return (
            self.db.query(PlannedWorkout)
            .filter(
                PlannedWorkout.week_id == week_id,
                PlannedWorkout.scheduled_date == scheduled_date,
            )
            .first()
        )

    def create(
        self,
        workout: PlannedWorkout,
    ) -> PlannedWorkout:

        self.db.add(workout)
        self.db.commit()
        self.db.refresh(workout)

        return workout