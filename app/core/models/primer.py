from pydantic import BaseModel

from app.core.models.multimedia_file import MultimediaFile


class Primer(BaseModel):
    content: MultimediaFile | str
