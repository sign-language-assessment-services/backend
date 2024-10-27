from pydantic import BaseModel, Field

from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice


class Exercise(BaseModel):
    position: int = Field(ge=0)
    question: MultimediaFile | str
    answer: MultipleChoice | str
