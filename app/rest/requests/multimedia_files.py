from pydantic import BaseModel

from app.core.models.media_types import MediaType


class CreateMultimediaFileRequest(BaseModel):
    media_type: MediaType
