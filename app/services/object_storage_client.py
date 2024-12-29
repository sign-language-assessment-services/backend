from typing import Annotated, cast

import requests
from fastapi import Depends, HTTPException
from minio import Minio
from minio.credentials import WebIdentityProvider

from app.config import Settings
from app.core.models.bucket_object import BucketObject
from app.core.models.minio_location import MinioLocation
from app.rest.settings import get_settings


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

    def list_folders(self, bucket_name: str, folder: str | None = None) -> list[str]:
        if folder:
            folder += "/"
        return [
            item.object_name.rstrip("/")
            for item in self.minio.list_objects(bucket_name=bucket_name, prefix=folder)
            if item.is_dir
        ]

    def list_files(self, bucket_name: str, folder: str) -> list[BucketObject]:
        if folder:
            folder += "/"
        return [
            BucketObject(name=item.object_name, content_type=item.metadata["content-type"])
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
