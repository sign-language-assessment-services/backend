from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.models.user import User
from app.dependencies import get_current_user, get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.requests.choices import CreateChoiceRequest
from app.rest.responses.choices import CreateChoiceResponse, GetChoiceResponse, ListChoiceResponse
from app.services.choice_service import ChoiceService

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["Choices"]
)


@router.post(
    "/choices/",
    response_model=CreateChoiceResponse,
    status_code=status.HTTP_200_OK
)
async def create_choice(
        data: CreateChoiceRequest,
        choice_service: Annotated[ChoiceService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    choice = choice_service.create_choice(
        session=db_session,
        multimedia_file_id=data.multimedia_file_id
    )
    return choice


@router.get(
    "/choices/{choice_id}",
    response_model=GetChoiceResponse,
    status_code=status.HTTP_200_OK
)
async def get_choice(
        choice_id: UUID,
        choice_service: Annotated[ChoiceService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    choice = choice_service.get_choice_by_id(
        session=db_session,
        choice_id=choice_id
    )
    if not choice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The choice id '{choice_id}' was not found."
        )
    return choice


@router.get(
    "/choices/",
    response_model=list[ListChoiceResponse],
    status_code=status.HTTP_200_OK
)
async def list_choices(
        choice_service: Annotated[ChoiceService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    choices = choice_service.list_choices(session=db_session)
    return choices
