from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.question import Question
from app.core.models.question_type import QuestionType
from app.core.models.submission import Submission


class Exercise(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    points: int
    question: Question
    question_type: QuestionType
    submissions: list[Submission] = Field(default_factory=list)
