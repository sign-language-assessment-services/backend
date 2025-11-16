from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.orm import Session

from app.core.models.role import UserRole
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import require_roles
from app.rest.responses.multimedia_files import (
    CreateMultimediaFileResponse, GetMultimediaFileResponse, ListMultimediaFileResponse
)
from app.services.multimedia_file_service import MultimediaFileService

router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(require_roles([UserRole.FRONTEND]))
    ],
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
        db_session: Annotated[Session, Depends(get_db_session)]
):
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
        db_session: Annotated[Session, Depends(get_db_session)]
):
    multimedia_file = multimedia_file_service.get_multimedia_file_by_id(
        session=db_session,
        multimedia_file_id=multimedia_file_id
    )
    return multimedia_file


@router.get(
    "/multimedia_files/",
    response_model=list[ListMultimediaFileResponse],
    status_code=status.HTTP_200_OK
)
async def list_multimedia_files(
        multimedia_file_service: Annotated[MultimediaFileService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    multimedia_files = multimedia_file_service.list_multimedia_files(session=db_session)
    return multimedia_files
