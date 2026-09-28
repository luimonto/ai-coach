from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.athlete import Athlete
from app.schemas.athlete import AthleteProfile


class AthleteRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_external_id(
        self,
        external_id: str,
    ) -> Athlete | None:

        return self.db.scalar(
            select(Athlete).where(Athlete.external_id == external_id)
        )

    def get_or_create(
        self,
        external_id: str
    ) -> Athlete:

        athlete = self.get_by_external_id(
            external_id
        )

        if athlete:
            return athlete

        athlete = Athlete(external_id=external_id)

        self.db.add(athlete)
        self.db.flush()

        return athlete

    def update_profile(
        self,
        athlete: Athlete,
        profile: AthleteProfile,
    ) -> Athlete:
        for field, value in profile.model_dump().items():
            setattr(athlete, field, value)

        self.db.commit()
        self.db.refresh(athlete)
        return athlete
