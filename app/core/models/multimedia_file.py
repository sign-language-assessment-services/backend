from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


class MultimediaFile(BaseModel):
    id: UUID = Field(default_factory=UUID)
    created_at: datetime = Field(default_factory=datetime.now)

    location: MinioLocation
    content_type: MediaType
