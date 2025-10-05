from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.models.user import User
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import get_current_user
from app.rest.requests.primers import CreatePrimerRequest
from app.rest.responses.primers import CreatePrimerResponse, GetPrimerResponse, ListPrimerResponse
from app.services.primer_service import PrimerService

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["Primers"]
)


@router.post(
    "/primers/",
    response_model=CreatePrimerResponse,
    status_code=status.HTTP_200_OK
)
async def create_primer(
        data: CreatePrimerRequest,
        primer_service: Annotated[PrimerService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    primer = primer_service.create_primer(
        session=db_session,
        multimedia_file_id=data.multimedia_file_id
    )
    return primer


@router.get(
    "/primers/{primer_id}",
    response_model=GetPrimerResponse,
    status_code=status.HTTP_200_OK
)
async def get_primer(
        primer_id: UUID,
        primer_service: Annotated[PrimerService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    primer = primer_service.get_primer_by_id(
        session=db_session,
        primer_id=primer_id
    )
    if not primer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The primer id '{primer_id}' was not found."
        )
    return primer


@router.get(
    "/primers/",
    response_model=list[ListPrimerResponse],
    status_code=status.HTTP_200_OK
)
async def list_primers(
        primer_service: Annotated[PrimerService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    primers = primer_service.list_primers(session=db_session)
    return primers
