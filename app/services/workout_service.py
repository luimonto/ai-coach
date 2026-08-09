from app.services.ai_service import AIService
from app.services.garmin_service import GarminService
from app.schemas.workout_summary import WorkoutSummary


class WorkoutService:

    def __init__(self, ai_service: AIService, garmin_service: GarminService):
        self.ai_service = ai_service
        self.garmin_service = garmin_service

    def get_current_workouts(self) -> list[WorkoutSummary]:
        workouts = self.garmin_service.get_workouts()
        return [
            WorkoutSummary(
                workout_id=workout["workoutId"],
                workout_name=workout["workoutName"],
                sport_type_id=workout["sportType"]["sportTypeId"],
                sport_type_key=workout["sportType"]["sportTypeKey"],
                description=workout.get("description"),
                estimated_duration_seconds=workout.get(
                    "estimatedDurationInSeconds"
                ),
                estimated_distance_meters=workout.get(
                    "estimatedDistanceInMeters"
                ),
                created_date=workout.get("createdDate"),
                update_date=workout.get("updateDate"),
            )
            for workout in workouts
        ]

    def create_schedule(self, user_goal: str) -> list[dict]:

        schedule = self.ai_service.generate_schedule(
            user_goal
        )
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