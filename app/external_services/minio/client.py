import logging
from typing import Annotated, BinaryIO, cast

import requests
from fastapi import Depends, HTTPException
from minio import Minio
from minio.credentials import WebIdentityProvider

from app.config import Settings
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.settings import get_settings

logger = logging.getLogger(__name__)


class ObjectStorageClient:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings
        self.minio = Minio(
            endpoint=settings.data_endpoint,
            secure=settings.data_secure,
            credentials=WebIdentityProvider(
                jwt_provider_func=self._fetch_access_token,
                sts_endpoint=settings.data_sts_endpoint,
            )
        )

    def get_presigned_url(self, location: MinioLocation) -> str:
        logger.debug(
            f"Getting presigned URL for {location.bucket}/{location.key}"
        )
        try:
            presigned_url = self.minio.get_presigned_url(
                method="GET",
                bucket_name=location.bucket,
                object_name=location.key
            )
            return cast(str, presigned_url)
        except Exception as exc:
            logger.exception(
                f"Failed to get presigned URL for "
                f"{location.bucket}/{location.key}"
            )
            raise HTTPException(
                status_code=503, detail=f"Minio not reachable. {exc}"
            ) from exc

    def add_object(self, location: MinioLocation, data: BinaryIO, media_type: str) -> None:
        self.minio.put_object(
            bucket_name=location.bucket,
            object_name=location.key,
            data=data,
            length=-1,
            part_size=16 * 1024 * 1024,  # 16 MiB
            content_type=media_type
        )

    def list_folders(self, bucket_name: str, folder: str | None = None) -> list[str]:
        if folder:
            folder += "/"
        return [
            item.object_name.rstrip("/")
            for item in self.minio.list_objects(bucket_name=bucket_name, prefix=folder)
            if item.is_dir
        ]

    def list_files(self, bucket_name: str, folder: str) -> list[MultimediaFile]:
        if folder:
            folder += "/"

        return [
            MultimediaFile(
                location=MinioLocation(
                    bucket=item.bucket_name,
                    key=item.object_name
                ),
                media_type=MediaType(item.metadata["content-type"])
            )
            for item in self.minio.list_objects(bucket_name=bucket_name, prefix=folder, include_user_meta=True)
            if not item.is_dir
        ]

    def _fetch_access_token(self) -> dict:
        return requests.post(
            url=self.settings.token_endpoint,
            data={
                "grant_type": "client_credentials",
                "client_id": self.settings.client_id,
                "client_secret": self.settings.client_secret,
            },
            timeout=10.0
        ).json()
