from uuid import UUID

from pydantic import BaseModel, field_validator

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer


class CreateAssessmentResponse(BaseModel):
    id: UUID
    name: str


class GetAssessmentResponse(BaseModel):
    id: UUID
    name: str
    tasks: list[Primer | Exercise]

    @field_validator("tasks", mode="after")
    @classmethod
    def compute_multimedia_file_id(cls, value) -> list[dict[str, str | UUID]]:
        return [
            {
                "id": task.id,
                "task_type": task.__class__.__name__.lower()
            }
            for task in value
        ]


class ListAssessmentResponse(BaseModel):
    id: UUID
    name: str
