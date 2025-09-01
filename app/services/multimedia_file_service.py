from typing import Annotated, BinaryIO
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.external_services.minio.client import ObjectStorageClient
from app.repositories.multimedia_files import (
    add_multimedia_file, get_multimedia_file, list_multimedia_files
)
from app.settings import get_settings


class MultimediaFileService:
    def __init__(
            self,
            settings: Annotated[Settings, Depends(get_settings)],
            object_storage_client: Annotated[ObjectStorageClient, Depends()],
    ):
        self.settings = settings
        self.object_storage_client = object_storage_client

    def create_multimedia_file(
            self,
            session: Session,
            file: BinaryIO,
            media_type: MediaType
    ) -> MultimediaFile:
        key = uuid4()
        minio_location = MinioLocation(
            bucket=self.settings.data_bucket_name,
            key=str(key)
        )
        self.object_storage_client.add_object(
            location=minio_location,
            data=file,
            media_type=media_type
        )
        multimedia_file = MultimediaFile(
            id=key,
            location=minio_location,
            media_type=media_type
        )
        add_multimedia_file(
            session=session,
            multimedia_file=multimedia_file
        )
        return multimedia_file

    def get_multimedia_file_by_id(self, session: Session, multimedia_file_id: UUID) -> MultimediaFile | None:
        multimedia_file = get_multimedia_file(session=session, _id=multimedia_file_id)
        multimedia_file.url = self._get_multimedia_file_url(multimedia_file.location)
        return multimedia_file

    def list_multimedia_files(self, session: Session) -> list[MultimediaFile]:
        multimedia_files = list_multimedia_files(session=session)
        for multimedia_file in multimedia_files:
            multimedia_file.url = self._get_multimedia_file_url(multimedia_file.location)
        return multimedia_files

    def _get_multimedia_file_url(self, location: MinioLocation) -> str:
        return self.object_storage_client.get_presigned_url(location=location)
