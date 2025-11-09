from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.models.role import UserRole
from app.core.models.user import User
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import get_current_user
from app.rest.requests.multiple_choices import CreateMultipleChoiceRequest
from app.rest.responses.multiple_choices import (
    CreateMultipleChoiceResponse, GetMultipleChoiceResponse, ListMultipleChoiceResponse
)
from app.services.multiple_choice_service import MultipleChoiceService

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["Multiple Choices"]
)


@router.post(
    "/multiple_choices/",
    response_model=CreateMultipleChoiceResponse,
    status_code=status.HTTP_200_OK
)
async def create_multiple_choice(
        data: CreateMultipleChoiceRequest,
        multiple_choice_service: Annotated[MultipleChoiceService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    if UserRole.FRONTEND_ACCESS.value not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    multiple_choice = multiple_choice_service.create_multiple_choice(
        session=db_session,
        choice_ids=data.choice_ids,
        correct_choice_ids=data.correct_choice_ids
    )
    return multiple_choice


@router.get(
    "/multiple_choices/{multiple_choice_id}",
    response_model=GetMultipleChoiceResponse,
    status_code=status.HTTP_200_OK
)
async def get_multiple_choice(
        multiple_choice_id: UUID,
        multiple_choice_service: Annotated[MultipleChoiceService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    if UserRole.FRONTEND_ACCESS.value not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    multiple_choice = multiple_choice_service.get_multiple_choice_by_id(
        session=db_session,
        multiple_choice_id=multiple_choice_id
    )
    if not multiple_choice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The multiple_choice id '{multiple_choice_id}' was not found."
        )
    return multiple_choice


@router.get(
    "/multiple_choices/",
    response_model=list[ListMultipleChoiceResponse],
    status_code=status.HTTP_200_OK
)
async def list_multiple_choices(
        multiple_choice_service: Annotated[MultipleChoiceService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    if UserRole.FRONTEND_ACCESS.value not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    multiple_choices = multiple_choice_service.list_multiple_choices(session=db_session)
    return multiple_choices
