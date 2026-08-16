from collections import defaultdict

from app.schemas.activity_summary import ActivitySummary
from app.schemas.training_summary import (
    SportSummary,
    TrainingSummary,
)


class TrainingAnalysisService:

    def build_summary(
        self,
        activities: list[ActivitySummary],
        period_days: int,
    ) -> TrainingSummary:

        sport_data = defaultdict(
            lambda: {
                "sessions": 0,
                "duration": 0.0,
                "distance": 0.0,
                "heart_rates": [],
                "max_heart_rate": None,
            }
        )

        for activity in activities:
            sport = activity.sport_type_key

            data = sport_data[sport]

            data["sessions"] += 1

            if activity.duration_seconds:
                data["duration"] += activity.duration_seconds

            if activity.distance_meters:
                data["distance"] += activity.distance_meters

            if activity.average_heart_rate:
                data["heart_rates"].append(
                    activity.average_heart_rate
                )

            if activity.max_heart_rate:
                current_max = data["max_heart_rate"]

                if current_max is None:
                    data["max_heart_rate"] = (
                        activity.max_heart_rate
                    )
                else:
                    data["max_heart_rate"] = max(
                        current_max,
                        activity.max_heart_rate,
                    )

        sports = []

        for sport, data in sport_data.items():

            average_hr = None

            if data["heart_rates"]:
                average_hr = (
                    sum(data["heart_rates"])
                    / len(data["heart_rates"])
                )

            sports.append(
                SportSummary(
                    sport_type=sport,
                    sessions=data["sessions"],
                    total_duration_seconds=data["duration"],
                    total_distance_meters=data["distance"],
                    average_heart_rate=average_hr,
                    max_heart_rate=data["max_heart_rate"],
                )
            )

        return TrainingSummary(
            period_days=period_days,
            total_sessions=len(activities),
            total_duration_seconds=sum(
                activity.duration_seconds or 0
                for activity in activities
            ),
            total_distance_meters=sum(
                activity.distance_meters or 0
                for activity in activities
            ),
            sports=sports,
            recent_activities=activities[:10],
        )