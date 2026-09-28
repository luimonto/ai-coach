from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class ActivitySyncItem(BaseModel):
    """Normalized completed activity supplied by the client."""

    garmin_activity_id: int = Field(gt=0)
    activity_name: str = Field(min_length=1, max_length=255)
    sport_type_key: str = Field(min_length=1, max_length=100)
    start_time: datetime
    duration_seconds: int | None = Field(default=None, ge=0)
    distance_meters: float | None = Field(default=None, ge=0)
    average_heart_rate: int | None = Field(default=None, ge=0)
    max_heart_rate: int | None = Field(default=None, ge=0)
    calories: float | None = Field(default=None, ge=0)


class ActivitySyncRequest(BaseModel):
    external_id: str = Field(min_length=1, max_length=255)
    activities: list[ActivitySyncItem] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def activity_ids_are_unique(self) -> "ActivitySyncRequest":
        ids = [activity.garmin_activity_id for activity in self.activities]
        if len(ids) != len(set(ids)):
            raise ValueError("garmin_activity_ids_must_be_unique")
        return self


class ActivitySyncResponse(BaseModel):
    created: int
    updated: int
    removed: int
    retained: int
