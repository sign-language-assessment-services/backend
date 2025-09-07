from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAssessmentRequest(BaseModel):
    name: str
    deadline: datetime | None = Field(default=None)
    max_attempts: int | None = Field(default=None)
    tasks: list[UUID] = Field(default_factory=list)
