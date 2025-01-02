from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, computed_field, Field, field_validator

from app.core.models.question import Question
from app.core.models.question_type import QuestionType


class Exercise(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    points: int
    question: Question
    question_type: QuestionType


class ExerciseResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    points: int
    question: dict[str, UUID | str] | Question
    question_type: QuestionType = Field(exclude=True)

    @field_validator("question", mode="before")
    @classmethod
    def compute_question_response(cls, value):
        return {
            "multimedia_file_id": value.content.id,
            "media_type": value.content.media_type.value
        }

    @computed_field
    @property
    def choices(self) -> list[dict[str, UUID | str]]:
        return [
            {
                "multimedia_file_id": choice.content.id,
                "media_type": choice.content.media_type.value
            }
            for number, choice in enumerate(
                self.question_type.content.choices, start=1  # pylint: disable=no-member
            )
        ]
