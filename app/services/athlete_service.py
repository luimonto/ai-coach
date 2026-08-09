from app.schemas.athlete import AthleteProfile


class AthleteService:

    def __init__(self):
        self._profile = AthleteProfile()

    def get_profile(self) -> AthleteProfile:
        return self._profile

    def update_profile(self, profile: AthleteProfile) -> AthleteProfile:
        self._profile = profile
        return self._profile