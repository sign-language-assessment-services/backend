from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models.answer import Answer
from app.core.models.exercise import Exercise


class Submission(BaseModel):
    id: UUID = Field(default_factory=UUID)
    created_at: datetime = Field(default_factory=datetime.now)

    user_id: str
    exercise: Exercise
    answer: Answer
