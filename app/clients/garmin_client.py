from garminconnect import Garmin
from app.core.config import get_settings


def get_garmin_client() -> Garmin:
    settings = get_settings()
    api = Garmin(
        email=settings.garmin_email,
        password=settings.garmin_password,
    )
    api.login()
    return api