from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer


class Assessment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    name: str
    tasks: list[Primer | Exercise] = Field(default_factory=list)


class AssessmentListResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str


class AssessmentResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    tasks: list[dict[str, UUID | str]]

    @field_validator("tasks", mode="before")
    @classmethod
    def extract_task_ids(cls, value):
        return [
            {
                "id": task.id,
                "task_type": task.__class__.__name__.lower()
            }
            for task in value
        ]
