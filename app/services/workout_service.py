from app.services.ai_service import AIService
from app.services.garmin_service import GarminService
from app.schemas.workout_summary import WorkoutSummary
from app.services.athlete_service import AthleteService
from app.schemas.coach import AthleteContext
from app.schemas.activity_summary import ActivitySummary


class WorkoutService:

    def __init__(self, ai_service: AIService, garmin_service: GarminService, athlete_service: AthleteService):
        self.ai_service = ai_service
        self.garmin_service = garmin_service
        self.athlete_service = athlete_service

    def get_recent_workouts(
        self,
        limit: int = 20,
    ) -> list[WorkoutSummary]:
        workouts = self.garmin_service.get_workouts()

        summaries = [
            WorkoutSummary(
                workout_id=workout["workoutId"],
                workout_name=workout["workoutName"],
                sport_type_id=workout["sportType"]["sportTypeId"],
                sport_type_key=workout["sportType"]["sportTypeKey"],
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

        return summaries[:limit] if limit > 0 else summaries


    def get_current_workouts(self) -> list[WorkoutSummary]:
        return self.get_recent_workouts()

    def build_athlete_context(
            self,
            limit: int = 20,
    ) -> AthleteContext:
        recent_activities = self.get_recent_activities(limit=limit)
        return self.athlete_service.build_context(
            recent_activities=recent_activities
        )

    def generate_training_schedule(
        self,
        user_goal: str
    ):
        athlete_context = self.build_athlete_context()

        return self.ai_service.generate_schedule(
            user_goal=user_goal,
            athlete_context=athlete_context,
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
                workout_payload=entry["workoutData"],
                target_date=entry["scheduleDate"],
            )

        return schedule

    def get_recent_activities(
        self,
        limit: int = 20,
    ) -> list[ActivitySummary]:

        activities = self.garmin_service.get_recent_activities(limit)

        return [
            ActivitySummary(
                activity_id=activity["activityId"],
                activity_name=activity.get(
                    "activityName",
                    "Unknown Activity",
                ),
                sport_type_key=activity.get(
                    "activityType",
                    {}).get(
                        "typeKey",
                        "unknown",
                    ),
                start_time=activity.get("startTimeLocal"),
                duration_seconds=activity.get("duration"),
                distance_meters=activity.get("distance"),
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