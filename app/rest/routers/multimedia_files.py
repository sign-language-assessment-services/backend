from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.models.user import User
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import get_current_user
from app.rest.responses.multimedia_files import (
    CreateMultimediaFileResponse, GetMultimediaFileResponse, ListMultimediaFileResponse
)
from app.services.multimedia_file_service import MultimediaFileService

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["Multimedia Files"],
)


@router.post(
    "/multimedia_files/",
    response_model=CreateMultimediaFileResponse,
    status_code=status.HTTP_200_OK
)
async def create_multimedia_file(
        file: UploadFile,
        multimedia_file_service: Annotated[MultimediaFileService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session),
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )
    multimedia_file = multimedia_file_service.create_multimedia_file(
        session=db_session,
        file=file.file,
        media_type=file.content_type
    )
    return multimedia_file


@router.get(
    "/multimedia_files/{multimedia_file_id}",
    response_model=GetMultimediaFileResponse,
    status_code=status.HTTP_200_OK
)
async def get_multimedia_file(
        multimedia_file_id: UUID,
        multimedia_file_service: Annotated[MultimediaFileService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    multimedia_file = multimedia_file_service.get_multimedia_file_by_id(
        session=db_session,
        multimedia_file_id=multimedia_file_id
    )
    if not multimedia_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The multimedia file id '{multimedia_file_id}' was not found."
        )
    return multimedia_file


@router.get(
    "/multimedia_files/",
    response_model=list[ListMultimediaFileResponse],
    status_code=status.HTTP_200_OK
)
async def list_multimedia_files(
        multimedia_file_service: Annotated[MultimediaFileService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    multimedia_files = multimedia_file_service.list_multimedia_files(session=db_session)
    return multimedia_files
