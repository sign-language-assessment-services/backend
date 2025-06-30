from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from app.core.models.multiple_choice_answer import MultipleChoiceAnswer


class ExerciseSubmission(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime | None = Field(default=None)

    answer: MultipleChoiceAnswer
    score: float | None = Field(default=None)
    assessment_submission_id: UUID
    exercise_id: UUID

    @field_validator("id", mode="before")
    @classmethod
    def set_id_if_none(cls, value: UUID | None) -> UUID:
        if value is None:
            return uuid4()
        return value
