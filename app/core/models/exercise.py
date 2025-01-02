from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, computed_field

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
            "id": value.content.id,
            "url": "http://example.com/question.mp4"
        }

    @computed_field
    @property
    def choices(self) -> list[dict[str, UUID | str]]:
        return [
            {
                "id": choice.id,
                "url": f"http://example.com/choice_{number}.mp4"
            }
            for number, choice in enumerate(
                self.question_type.content.choices, start=1
            )
        ]
