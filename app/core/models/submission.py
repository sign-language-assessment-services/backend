from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.multiple_choice_answer import MultipleChoiceAnswer


class Submission(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    user_name: str
    exercise_id: UUID
    multiple_choice_id: UUID
    answer: MultipleChoiceAnswer
