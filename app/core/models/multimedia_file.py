from pydantic import BaseModel

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


class MultimediaFile(BaseModel):
    location: MinioLocation
    content_type: MediaType
