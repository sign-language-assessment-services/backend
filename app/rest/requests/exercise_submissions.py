from uuid import UUID

from pydantic import BaseModel, Field


class UpsertExerciseSubmissionRequest(BaseModel):
    id: UUID | None = Field(default=None)
    answer: list[UUID]
