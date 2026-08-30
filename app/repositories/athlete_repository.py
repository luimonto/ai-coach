from sqlalchemy.orm import Session
from app.db.models.athlete import Athlete


class AthleteRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_external_id(
        self,
        external_id: str,
    ) -> Athlete | None:

        return (
            self.db.query(Athlete)
            .filter(
                Athlete.external_id == external_id
            )
            .first()
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

        athlete = Athlete(
            external_id=external_id
        )

        self.db.add(athlete)
        self.db.flush()

        return athlete