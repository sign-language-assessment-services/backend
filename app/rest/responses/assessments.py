from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


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


class AssessmentListResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
