from datetime import date, datetime, time, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.athlete import Athlete
from app.db.models.planned_workout import PlannedWorkout
from app.db.models.training_plan import TrainingPlan
from app.db.models.training_plan_week import TrainingPlanWeek
from app.repositories.activity_repository import ActivityRepository
from app.repositories.athlete_repository import AthleteRepository
from app.repositories.planned_workout_repository import PlannedWorkoutRepository
from app.repositories.training_plan_repository import TrainingPlanRepository
from app.schemas.activity_summary import ActivitySummary
from app.schemas.coach import AthleteContext
from app.schemas.training_plan import (
    CurrentWeekResponse,
    CurrentWeekWorkoutsResponse,
    PlannedWorkoutResponse,
    TrainingPlanSchema,
    WeeklyPlan,
    WorkoutDetail,
)
from app.services.ai_service import AIService
from app.services.athlete_service import AthleteService
from app.services.training_analysis_service import TrainingAnalysisService


class WorkoutService:
    """Coordinates persisted coaching state and AI generation for one athlete."""

    ACTIVITY_CONTEXT_LIMIT = 20

    def __init__(
        self,
        db: Session,
        ai_service: AIService,
        athlete_service: AthleteService,
        training_analysis_service: TrainingAnalysisService,
        athlete_repository: AthleteRepository,
        training_plan_repository: TrainingPlanRepository,
        planned_workout_repository: PlannedWorkoutRepository,
        activity_repository: ActivityRepository,
    ):
        self.db = db
        self.ai_service = ai_service
        self.athlete_service = athlete_service
        self.training_analysis_service = training_analysis_service
        self.athlete_repository = athlete_repository
        self.training_plan_repository = training_plan_repository
        self.planned_workout_repository = planned_workout_repository
        self.activity_repository = activity_repository

    def generate_training_roadmap(
        self,
        external_id: str,
        user_goal: str,
    ) -> TrainingPlanSchema:
        athlete = self.athlete_repository.get_or_create(external_id)
        existing_plan = self.training_plan_repository.get_active_plan(athlete.id)
        if existing_plan:
            return self._plan_to_schema(existing_plan)

        training_plan = self.ai_service.generate_training_roadmap(
            user_goal=user_goal,
            athlete_context=self._build_athlete_context(athlete),
        )
        db_plan = self.training_plan_repository.create(
            athlete_id=athlete.id,
            goal=user_goal,
            start_date=date.today(),
            duration_weeks=training_plan.duration_weeks,
        )

        for week in training_plan.weeks:
            week_start = db_plan.start_date + timedelta(weeks=week.week - 1)
            self.db.add(
                TrainingPlanWeek(
                    training_plan_id=db_plan.id,
                    week_number=week.week,
                    start_date=week_start,
                    end_date=week_start + timedelta(days=6),
                    objective=week.objective,
                    focus=week.focus,
                    intensity=week.intensity,
                    status="active" if week.week == 1 else "pending",
                )
            )

        self.db.commit()
        return training_plan

    def generate_workout_detail(
        self,
        external_id: str,
        week_number: int,
        scheduled_date: date,
    ) -> WorkoutDetail:
        athlete, training_plan = self._get_active_plan(external_id)
        week = self.training_plan_repository.get_week(training_plan.id, week_number)
        if week is None:
            raise HTTPException(status_code=404, detail="training_plan_week_not_found")
        if not week.start_date <= scheduled_date <= week.end_date:
            raise HTTPException(status_code=400, detail="scheduled_date_outside_plan_week")

        existing = self.planned_workout_repository.get_by_week_and_date(
            week_id=week.id,
            scheduled_date=scheduled_date,
        )
        if existing:
            return WorkoutDetail.model_validate(existing.workout_data)

        workout_detail = self.ai_service.expand_workout_details(
            roadmap_week=self._week_to_schema(week),
            athlete_context=self._build_athlete_context(athlete),
        )
        self.planned_workout_repository.create(
            PlannedWorkout(
                week_id=week.id,
                scheduled_date=scheduled_date,
                workout_type=workout_detail.workout_type,
                workout_name=workout_detail.workout_name,
                workout_data=workout_detail.model_dump(),
                status="planned",
            )
        )
        return workout_detail

    def get_current_week(self, external_id: str) -> CurrentWeekResponse:
        training_plan, week = self._get_current_plan_week(external_id)
        return CurrentWeekResponse(
            training_plan_id=training_plan.id,
            week_id=week.id,
            week_number=week.week_number,
            start_date=week.start_date,
            end_date=week.end_date,
            objective=week.objective,
            focus=week.focus,
            intensity=week.intensity,
            status=week.status,
        )

    def get_current_week_workouts(
        self,
        external_id: str,
    ) -> CurrentWeekWorkoutsResponse:
        training_plan, week = self._get_current_plan_week(external_id)
        return CurrentWeekWorkoutsResponse(
            training_plan_id=training_plan.id,
            week_id=week.id,
            week_number=week.week_number,
            start_date=week.start_date,
            end_date=week.end_date,
            objective=week.objective,
            focus=week.focus,
            intensity=week.intensity,
            status=week.status,
            workouts=[self._planned_workout_to_response(workout) for workout in week.workouts],
        )

    def _build_athlete_context(self, athlete: Athlete) -> AthleteContext:
        activities = self.activity_repository.get_recent_by_athlete(
            athlete_id=athlete.id,
            limit=self.ACTIVITY_CONTEXT_LIMIT,
            since=datetime.combine(date.today() - timedelta(days=14), time.min),
        )
        summaries = [
            ActivitySummary(
                activity_id=activity.garmin_activity_id,
                activity_name=activity.activity_name,
                sport_type_key=activity.sport_type_key,
                start_time=activity.start_time,
                duration_seconds=activity.duration_seconds,
                distance_meters=activity.distance_meters,
                average_heart_rate=activity.average_heart_rate,
                max_heart_rate=activity.max_heart_rate,
                calories=activity.calories,
            )
            for activity in activities
        ]
        return self.athlete_service.build_context(
            athlete=athlete,
            recent_activities=summaries,
            training_summary=self.training_analysis_service.build_summary(
                activities=summaries,
                period_days=14,
            ),
        )

    def _get_active_plan(self, external_id: str) -> tuple[Athlete, TrainingPlan]:
        athlete = self.athlete_repository.get_by_external_id(external_id)
        if athlete is None:
            raise HTTPException(status_code=404, detail="athlete_not_found")

        training_plan = self.training_plan_repository.get_active_plan(athlete.id)
        if training_plan is None:
            raise HTTPException(status_code=404, detail="active_training_plan_not_found")
        return athlete, training_plan

    def _get_current_plan_week(
        self,
        external_id: str,
    ) -> tuple[TrainingPlan, TrainingPlanWeek]:
        _, training_plan = self._get_active_plan(external_id)
        days_since_start = max((date.today() - training_plan.start_date).days, 0)
        week_number = days_since_start // 7 + 1
        if week_number > training_plan.duration_weeks:
            raise HTTPException(status_code=404, detail="training_plan_finished")

        week = self.training_plan_repository.get_week(training_plan.id, week_number)
        if week is None:
            raise HTTPException(status_code=404, detail="training_plan_week_not_found")
        return training_plan, week

    @staticmethod
    def _plan_to_schema(plan: TrainingPlan) -> TrainingPlanSchema:
        return TrainingPlanSchema(
            duration_weeks=plan.duration_weeks,
            overall_objective=plan.goal,
            weeks=[WorkoutService._week_to_schema(week) for week in plan.weeks],
        )

    @staticmethod
    def _week_to_schema(week: TrainingPlanWeek) -> WeeklyPlan:
        return WeeklyPlan(
            week=week.week_number,
            objective=week.objective,
            focus=week.focus,
            intensity=week.intensity,
        )

    @staticmethod
    def _planned_workout_to_response(workout: PlannedWorkout) -> PlannedWorkoutResponse:
        return PlannedWorkoutResponse(
            id=workout.id,
            scheduled_date=workout.scheduled_date,
            workout_type=workout.workout_type,
            workout_name=workout.workout_name,
            workout_data=workout.workout_data,
            status=workout.status,
            garmin_workout_id=workout.garmin_workout_id,
        )
