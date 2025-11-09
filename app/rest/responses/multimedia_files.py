from uuid import UUID

from pydantic import BaseModel, HttpUrl, field_validator

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation


class CreateMultimediaFileResponse(BaseModel):
    id: UUID
    location: MinioLocation


class GetMultimediaFileResponse(BaseModel):
    id: UUID
    url: str
    media_type: MediaType

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        HttpUrl(value)
        return value


class ListMultimediaFileResponse(BaseModel):
    id: UUID
    url: str
    media_type: MediaType

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        HttpUrl(value)
        return value
