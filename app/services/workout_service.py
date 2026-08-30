from datetime import date, timedelta
import json
from fastapi import HTTPException
from sqlalchemy.orm import Session

from sqlalchemy.orm import Session

from app.repositories.athlete_repository import (
    AthleteRepository,
)

from app.repositories.training_plan_repository import (
    TrainingPlanRepository,
)
from app.schemas.activity_summary import ActivitySummary
from app.schemas.coach import AthleteContext
from app.schemas.training_plan import (
    PlannedWorkout,
    TrainingPlanSchema,
    WeeklyPlan,
    WorkoutDetail
)
from app.schemas.workout_summary import WorkoutSummary

from app.services.ai_service import AIService
from app.services.athlete_service import AthleteService
from app.services.garmin_service import GarminService
from app.services.training_analysis_service import (
    TrainingAnalysisService
)
from app.schemas.training_plan import CurrentWeekResponse
from app.db.models.athlete import Athlete
from app.db.models.training_plan import TrainingPlan
from app.db.models.training_plan_week import TrainingPlanWeek


class WorkoutService:

    def __init__(
        self,
        db: Session,
        ai_service: AIService,
        garmin_service: GarminService,
        athlete_service: AthleteService,
        training_analysis_service: TrainingAnalysisService,
        athlete_repository: AthleteRepository,
        training_plan_repository: TrainingPlanRepository
    ):
        self.db = db
        self.ai_service = ai_service
        self.garmin_service = garmin_service
        self.athlete_service = athlete_service
        self.training_analysis_service = (
            training_analysis_service
        )
        self.athlete_repository = athlete_repository
        self.training_plan_repository = training_plan_repository

    def get_recent_workouts(
        self,
        limit: int = 20,
    ) -> list[WorkoutSummary]:

        workouts = []
        try:
            workouts = self.garmin_service.get_workouts()
        except Exception as e:
            with open("garmin_test_data/workout_summary.json") as f:
                workouts = json.load(f)

        summaries = [
            WorkoutSummary(
                workout_id=workout["workoutId"],
                workout_name=workout["workoutName"],
                sport_type_id=workout["sportType"][
                    "sportTypeId"
                ],
                sport_type_key=workout["sportType"][
                    "sportTypeKey"
                ],
                description=workout.get("description"),
                estimated_duration_seconds=workout.get(
                    "estimatedDurationInSecs"
                ),
                estimated_distance_meters=workout.get(
                    "estimatedDistanceInMeters"
                ),
                created_date=workout.get("createdDate"),
                update_date=workout.get("updateDate"),
            )
            for workout in workouts
        ]

        return (
            summaries[:limit]
            if limit > 0
            else summaries
        )

    def get_current_workouts(
        self,
    ) -> list[WorkoutSummary]:
        return self.get_recent_workouts()

    def get_recent_activities(
        self,
        limit: int = 20,
    ) -> list[ActivitySummary]:
        activities = []
        try:
            activities = (
                        self.garmin_service
                        .get_recent_activities(limit)
                    )
        except Exception as e:
            with open("garmin_test_data/activity_summary.json") as f:
                activities = json.load(f)

        return [
            ActivitySummary(
                activity_id=activity["activityId"],
                activity_name=activity.get(
                    "activityName",
                    "Unknown Activity",
                ),
                sport_type_key=activity.get(
                    "activityType",
                    {},
                ).get(
                    "typeKey",
                    "unknown",
                ),
                start_time=activity.get(
                    "startTimeLocal"
                ),
                duration_seconds=activity.get(
                    "duration"
                ),
                distance_meters=activity.get(
                    "distance"
                ),
                average_heart_rate=activity.get(
                    "averageHR"
                ),
                max_heart_rate=activity.get(
                    "maxHR"
                ),
                calories=activity.get(
                    "calories"
                ),
            )
            for activity in activities
        ]

    def build_athlete_context(
        self,
        limit: int = 50,
    ) -> AthleteContext:

        recent_activities = (
            self.get_recent_activities(
                limit=limit
            )
        )

        training_summary = (
            self.training_analysis_service
            .build_summary(
                activities=recent_activities,
                period_days=14,
            )
        )

        return self.athlete_service.build_context(
            recent_activities=recent_activities,
            training_summary=training_summary,
        )

    def _save_plan_weeks(
        self,
        db_plan,
        training_plan: TrainingPlanSchema,
    ):
        from app.db.models.training_plan_week import (
            TrainingPlanWeek,
        )

        for week in training_plan.weeks:

            week_start = (
                db_plan.start_date
                + timedelta(
                    weeks=week.week - 1
                )
            )

            week_end = (
                week_start
                + timedelta(days=6)
            )

            db_week = TrainingPlanWeek(
                training_plan_id=db_plan.id,
                week_number=week.week,
                start_date=week_start,
                end_date=week_end,
                objective=week.objective,
                focus=week.focus,
                intensity=week.intensity,
                status=(
                    "active"
                    if week.week == 1
                    else "pending"
                ),
            )

            self.db.add(db_week)

    def _map_db_plan_to_schema(
        self,
        db_plan,
    ) -> TrainingPlanSchema:

        return TrainingPlanSchema(
            duration_weeks=db_plan.duration_weeks,
            overall_objective=db_plan.goal,
            weeks=[
                WeeklyPlan(
                    week=week.week_number,
                    objective=week.objective,
                    focus=week.focus,
                    intensity=week.intensity,
                )
                for week in db_plan.weeks
            ],
        )

    def generate_training_roadmap(
        self,
        external_id: str,
        user_goal: str,
    ) -> TrainingPlanSchema:

        athlete = self.athlete_repository.get_or_create(
            external_id
        )

        existing_plan = (
            self.training_plan_repository
            .get_active_plan(athlete.id)
        )

        if existing_plan:
            return self._map_db_plan_to_schema(
                existing_plan
            )

        athlete_context = (
            self.build_athlete_context()
        )

        training_plan = (
            self.ai_service.generate_training_roadmap(
                user_goal=user_goal,
                athlete_context=athlete_context,
            )
        )

        db_plan = (
            self.training_plan_repository.create(
                athlete_id=athlete.id,
                goal=user_goal,
                start_date=date.today(),
                duration_weeks=training_plan.duration_weeks,
            )
        )

        self._save_plan_weeks(
            db_plan=db_plan,
            training_plan=training_plan,
        )

        self.db.commit()

        return training_plan

    def build_workout_schedule(
        self,
        training_plan: TrainingPlanSchema,
        start_date: date | None = None,
    ) -> list[PlannedWorkout]:

        if start_date is None:
            start_date = date.today()

        workouts: list[PlannedWorkout] = []

        for week in training_plan.weeks:

            week_start = (
                start_date
                + timedelta(
                    weeks=week.week - 1
                )
            )

            # TEMPORARY:
            # One workout per week.
            #
            # We will replace this with the
            # real scheduling algorithm next.

            workouts.append(
                PlannedWorkout(
                    week=week.week,
                    date=week_start,
                    workout_type=(
                        week.focus[0]
                        if week.focus
                        else "training"
                    ),
                    objective=week.objective,
                    focus=(
                        ", ".join(week.focus)
                    ),
                    duration_minutes=None,
                )
            )

        return workouts

    def generate_workout_detail(
        self,
        roadmap_week: WeeklyPlan,
    ) -> WorkoutDetail:

        athlete_context = (
            self.build_athlete_context()
        )

        return (
            self.ai_service.expand_workout_details(
                roadmap_week=roadmap_week,
                athlete_context=athlete_context,
            )
        )

    def create_schedule(
        self,
        schedule: list[dict],
    ) -> list[dict]:

        self.garmin_service.cleanup_ai_workouts()

        for entry in schedule:

            if (
                "scheduleDate" not in entry
                or "workoutData" not in entry
            ):
                continue

            self.garmin_service.upload_and_schedule(
                workout_payload=entry[
                    "workoutData"
                ],
                target_date=entry[
                    "scheduleDate"
                ],
            )

        return schedule


    def get_training_summary(
        self,
        period_days: int = 14,
    ):

        activities = (
            self.get_recent_activities(
                limit=100
            )
        )

        return (
            self.training_analysis_service
            .build_summary(
                activities=activities,
                period_days=period_days,
            )
        )

    def get_current_week(
        self,
        external_id: str,
    ) -> CurrentWeekResponse:

        athlete = self.athlete_repository.get_by_external_id(
            external_id=external_id
        )

        if not athlete:
            raise HTTPException(
                status_code=404,
                detail="Athlete not found",
            )

        training_plan = self.training_plan_repository.get_active_plan(
            athlete_id=athlete.id
        )

        if not training_plan:
            raise HTTPException(
                status_code=404,
                detail="No active training plan found",
            )

        today = date.today()

        # Plan has not started yet
        if today < training_plan.start_date:
            week_number = 1
        else:
            days_since_start = (
                today - training_plan.start_date
            ).days

            week_number = (
                days_since_start // 7
            ) + 1

        # Plan has finished
        if week_number > training_plan.duration_weeks:
            raise HTTPException(
                status_code=404,
                detail="Training plan has finished",
            )

        current_week = self.training_plan_repository.get_week(
            training_plan_id=training_plan.id,
            week_number=week_number
        )

        if not current_week:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Week {week_number} "
                    "was not found in the training plan"
                ),
            )

        return CurrentWeekResponse(
            training_plan_id=training_plan.id,
            week_id=current_week.id,
            week_number=current_week.week_number,
            start_date=current_week.start_date,
            end_date=current_week.end_date,
            objective=current_week.objective,
            focus=current_week.focus,
            intensity=current_week.intensity,
            status=current_week.status,
        )