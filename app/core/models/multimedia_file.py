from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


class MultimediaFile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    location: MinioLocation
    media_type: MediaType
