from datetime import date
from garminconnect import Garmin


class GarminService:
    def __init__(self, client: Garmin):
        self.client = client

    def get_workouts(self) -> list[dict]:
        return self.client.get_workouts()

    def get_workout(self, workout_id: str) -> dict:
        return self.client.get_workout_by_id(workout_id)

    def get_scheduled_workouts(self) -> list[dict]:
        return self.client.get_scheduled_workouts()

    def cleanup_ai_workouts(self) -> int:
        deleted_count = 0
        workouts = self.client.get_workouts()

        for workout in workouts:
            name = workout.get("workoutName", "")
            workout_id = workout.get("workoutId")

            if name.startswith("AI ") and workout_id:
                self.client.delete_workout(workout_id)
                deleted_count += 1

        return deleted_count

    def upload_and_schedule(self, workout_payload: dict, target_date: str,) -> str:
        uploaded_id = None
        try:
            upload_response = self.client.upload_workout(
                workout_payload
            )
            uploaded_id = upload_response.get(
                "workoutId"
            )
            if not uploaded_id:
                raise KeyError(
                    "Workout ID missing from response payload"
                )
            self.client.schedule_workout(
                uploaded_id,
                target_date,
            )
            return uploaded_id
        except Exception:
            if uploaded_id:
                try:
                    self.client.delete_workout(
                        uploaded_id
                    )
                except Exception:
                    pass
            raise