from app.schemas.athlete import AthleteProfile
from app.schemas.coach import AthleteContext
from app.schemas.workout_summary import WorkoutSummary
from app.schemas.activity_summary import ActivitySummary


class AthleteService:

    def __init__(self):
        self._profile = AthleteProfile()

    def get_profile(self) -> AthleteProfile:
        return self._profile

    def update_profile(self, profile: AthleteProfile) -> AthleteProfile:
        self._profile = profile
        return self._profile

    def build_context(
        self,
        recent_activities: list[ActivitySummary],
    ) -> AthleteContext:
        return AthleteContext(
            profile=self._profile,
            recent_activities=recent_activities
        )