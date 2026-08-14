from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    llm_provider: str
    openai_api_key: str
    llm_endpoint: str
    model: str

    garmin_email: str
    garmin_password: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    database_url: str


@lru_cache()
def get_settings() -> Settings:
    """Get application settings."""
    return Settings() # type: ignore