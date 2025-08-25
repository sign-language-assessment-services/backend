from pydantic import BaseModel

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


class CreateMultimediaFileRequest(BaseModel):
    location: MinioLocation
    media_type: MediaType
