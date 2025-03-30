from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.fields import computed_field

from app.core.models.multiple_choice_answer import MultipleChoiceAnswer


class ExerciseSubmissionResponse(BaseModel):
    id: UUID
    user_id: UUID
    assessment_submission_id: UUID
    exercise_id: UUID
    answer: MultipleChoiceAnswer = Field(exclude=True)

    @computed_field
    @property
    def answers(self) -> list[UUID]:
        return self.answer.choices  # pylint: disable=no-member


class ExerciseSubmissionListResponse(BaseModel):
    id: UUID
