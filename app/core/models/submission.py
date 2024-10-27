from pydantic import BaseModel

from app.core.models.answer import Answer
from app.core.models.exercise import Exercise


class Submission(BaseModel):
    user_id: str
    exercise: Exercise
    answer: Answer
