from pydantic import BaseModel

from app.core.models.multiple_choice import MultipleChoice


class QuestionType(BaseModel):
    content: MultipleChoice
