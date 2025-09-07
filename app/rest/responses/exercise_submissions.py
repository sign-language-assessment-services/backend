from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.fields import computed_field

from app.core.models.multiple_choice_answer import MultipleChoiceAnswer


class GetExerciseSubmissionResponse(BaseModel):
    id: UUID
    assessment_submission_id: UUID
    exercise_id: UUID
    answer: MultipleChoiceAnswer = Field(exclude=True)

    @computed_field(
        description="List of answer IDs",
        json_schema_extra={
            "example": [
                "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            ]
        }
    )
    @property
    def answers(self) -> list[UUID]:
        return self.answer.choices  # pylint: disable=no-member


class ListExerciseSubmissionResponse(BaseModel):
    id: UUID
    assessment_submission_id: UUID
    exercise_id: UUID


class UpsertExerciseSubmissionResponse(BaseModel):
    id: UUID
