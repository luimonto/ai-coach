from datetime import date
from sqlalchemy.orm import Session
from app.db.models.training_plan import TrainingPlan
from app.db.models.training_plan_week import TrainingPlanWeek


class TrainingPlanRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_active_plan(
        self,
        athlete_id: int
    ) -> TrainingPlan | None:

        return (
            self.db.query(TrainingPlan)
            .filter(
                TrainingPlan.athlete_id == athlete_id,
                TrainingPlan.status == "active"
            )
            .order_by(
                TrainingPlan.created_at.desc()
            )
            .first()
        )

    def get_week(
        self,
        training_plan_id: int,
        week_number: int,
    ) -> TrainingPlanWeek | None:

        return (
            self.db.query(TrainingPlanWeek)
            .filter(
                TrainingPlanWeek.training_plan_id
                == training_plan_id,
                TrainingPlanWeek.week_number
                == week_number,
            )
            .first()
        )

    def create(
        self,
        athlete_id: int,
        goal: str,
        start_date: date,
        duration_weeks: int
    ) -> TrainingPlan:

        plan = TrainingPlan(
            athlete_id=athlete_id,
            goal=goal,
            start_date=start_date,
            duration_weeks=duration_weeks,
            status="active"
        )

        self.db.add(plan)
        self.db.flush()

        return plan