from pydantic import BaseModel

from app.core.models.multimedia_file import MultimediaFile


class Choice(BaseModel):
    content: MultimediaFile | str
    is_correct: bool
