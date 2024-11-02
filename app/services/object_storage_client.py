from typing import Annotated, cast

from fastapi import Depends, HTTPException
from minio import Minio

from app.config import Settings
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.settings import get_settings


class ObjectStorageClient:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.minio = Minio(
            endpoint=settings.data_endpoint,
            access_key=settings.data_root_user,
            secret_key=settings.data_root_password,
            secure=settings.data_secure,
        )

    def get_presigned_url(self, location: MinioLocation) -> str:
        try:
            presigned_url = self.minio.get_presigned_url(
                method="GET",
                bucket_name=location.bucket,
                object_name=location.key
            )
            return cast(str, presigned_url)
        except Exception as exc:
            raise HTTPException(
                status_code=503, detail=f"Minio not reachable. {exc}"
            ) from exc

    def list_folders(self, bucket_name: str, folder: str|None = None) -> list[str]:
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

        # todo: for iteration only for debugging purposes can be deleted
        for item in self.minio.list_objects(bucket_name=bucket_name, prefix=folder, include_user_meta=True):
            if not item.is_dir:
                print(item)

        return [
            MultimediaFile(
                location=MinioLocation(
                    bucket=item.bucket_name,
                    key=item.object_name
                ),
                content_type=item.metadata["content-type"]
            )
            for item in self.minio.list_objects(bucket_name=bucket_name, prefix=folder, include_user_meta=True)
            if not item.is_dir
        ]
