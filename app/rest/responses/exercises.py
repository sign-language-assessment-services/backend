from uuid import UUID

from pydantic import BaseModel, Field, computed_field, field_validator

from app.core.models.question import Question
from app.core.models.question_type import QuestionType


class CreateExerciseResponse(BaseModel):
    id: UUID


class GetExerciseResponse(BaseModel):
    id: UUID
    points: int
    question: dict[str, UUID | str] | Question
    question_type: QuestionType = Field(exclude=True)

    @field_validator("question", mode="before")
    @classmethod
    def compute_question_response(cls, value) -> dict[str, UUID | str]:
        return {
            "multimedia_file_id": value.content.id,
            "media_type": value.content.media_type.value
        }

    @computed_field
    @property
    def choices(self) -> list[dict[str, UUID | str]]:
        return [
            {
                "id": choice.id,
                "multimedia_file_id": choice.content.id,
                "media_type": choice.content.media_type.value
            }
            for number, choice in enumerate(
                self.question_type.content.choices, start=1  # pylint: disable=no-member
            )
        ]


class ListExerciseResponse(BaseModel):
    id: UUID
