from typing import Any
from pydantic import BaseModel


class WorkoutResponse(BaseModel):
    message: str
    schedule: list[dict[str, Any]]