from app.schemas.athlete import AthleteProfile
from app.schemas.coach import AthleteContext
from app.schemas.training_summary import TrainingSummary
from app.schemas.activity_summary import ActivitySummary
from app.db.models.athlete import Athlete
from app.repositories.athlete_repository import AthleteRepository


class AthleteService:

    def __init__(self, athlete_repository: AthleteRepository):
        self.athlete_repository = athlete_repository

    def get_profile(self, external_id: str) -> AthleteProfile | None:
        athlete = self.athlete_repository.get_by_external_id(external_id)
        return self.to_profile(athlete) if athlete else None

    def update_profile(
        self,
        external_id: str,
        profile: AthleteProfile,
    ) -> AthleteProfile:
        athlete = self.athlete_repository.get_or_create(external_id)
        athlete = self.athlete_repository.update_profile(athlete, profile)
        return self.to_profile(athlete)

    def build_context(
        self,
        athlete: Athlete,
        recent_activities: list[ActivitySummary],
        training_summary: TrainingSummary,
    ) -> AthleteContext:

        return AthleteContext(
            profile=self.to_profile(athlete),
            recent_activities=recent_activities,
            training_summary=training_summary,
        )

    @staticmethod
    def to_profile(athlete: Athlete) -> AthleteProfile:
        return AthleteProfile(
            name=athlete.name,
            age=athlete.age,
            height_cm=athlete.height_cm,
            weight_kg=athlete.weight_kg,
            experience_level=athlete.experience_level,
            primary_sport=athlete.primary_sport,
            secondary_sports=athlete.secondary_sports,
            weekly_training_days=athlete.weekly_training_days,
            preferred_training_days=athlete.preferred_training_days,
            goals=athlete.goals,
            notes=athlete.notes,
        )
