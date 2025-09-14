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

    @computed_field(
        description="Choices for the multiple choice question",
        json_schema_extra={
            "example": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "is_correct": True,
                    "position": 1
                }
            ]
        }
    )
    @property
    def choices(self) -> list[dict[str, UUID | int]]:
        return [
            {
                "id": choice.id,
                "position": choice.position,
                "multimedia_file_id": choice.content.id,
                "media_type": choice.content.media_type.value
            }
            for choice in self.question_type.content.choices  # pylint: disable=no-member
        ]


class ListExerciseResponse(BaseModel):
    id: UUID
    points: float
