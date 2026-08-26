from datetime import date, timedelta

from app.schemas.activity_summary import ActivitySummary
from app.schemas.coach import AthleteContext
from app.schemas.training_plan import (
    PlannedWorkout,
    TrainingPlanSchema,
)
from app.schemas.workout_detail import WorkoutDetail

from app.schemas.workout_summary import WorkoutSummary

from app.services.ai_service import AIService
from app.services.athlete_service import AthleteService
from app.services.garmin_service import GarminService
from app.services.training_analysis_service import (
    TrainingAnalysisService,
)


class WorkoutService:

    def __init__(
        self,
        ai_service: AIService,
        garmin_service: GarminService,
        athlete_service: AthleteService,
        training_analysis_service: TrainingAnalysisService,
    ):
        self.ai_service = ai_service
        self.garmin_service = garmin_service
        self.athlete_service = athlete_service
        self.training_analysis_service = (
            training_analysis_service
        )

    # ---------------------------------------------------------
    # GARMIN WORKOUTS
    # ---------------------------------------------------------

    def get_recent_workouts(
        self,
        limit: int = 20,
    ) -> list[WorkoutSummary]:

        workouts = self.garmin_service.get_workouts()

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

    # ---------------------------------------------------------
    # ATHLETE CONTEXT
    # ---------------------------------------------------------

    def get_recent_activities(
        self,
        limit: int = 20,
    ) -> list[ActivitySummary]:

        activities = (
            self.garmin_service
            .get_recent_activities(limit)
        )

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

    # ---------------------------------------------------------
    # AI - PLANNER
    # ---------------------------------------------------------

    def generate_training_roadmap(
        self,
        user_goal: str,
    ) -> TrainingPlanSchema:

        athlete_context = (
            self.build_athlete_context()
        )

        return (
            self.ai_service
            .generate_training_roadmap(
                user_goal=user_goal,
                athlete_context=athlete_context,
            )
        )

    # ---------------------------------------------------------
    # APPLICATION SCHEDULER
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # AI - DETAILER
    # ---------------------------------------------------------

    def generate_workout_detail(
        self,
        workout: PlannedWorkout,
    ) -> WorkoutDetail:

        athlete_context = (
            self.build_athlete_context()
        )

        return (
            self.ai_service
            .expand_workout_details(
                workout=workout,
                athlete_context=athlete_context,
            )
        )

    # ---------------------------------------------------------
    # GARMIN CREATION
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # TRAINING SUMMARY
    # ---------------------------------------------------------

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