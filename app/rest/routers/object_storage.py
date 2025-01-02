from http.client import HTTPException
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.authorization.auth_bearer import JWTBearer
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.services.multimedia_file_service import MultimediaFileService
from app.services.object_storage_client import ObjectStorageClient

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.get("/object-storage/{multimedia_file_id}")
async def get_object_storage_url(
        multimedia_file_id: UUID,
        object_storage_client: Annotated[ObjectStorageClient, Depends()],
        multimedia_file_service: Annotated[MultimediaFileService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> dict[str, str]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    multimedia_file = multimedia_file_service.get_multimedia_file_by_id(db_session, multimedia_file_id)
    if not multimedia_file:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return {
        "url": object_storage_client.get_presigned_url(location=multimedia_file.location),
        "media_type": multimedia_file.media_type
    }
