from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.models.role import UserRole
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import require_roles
from app.rest.responses.users import GetUserInfoResponse, ListUsersResponse
from app.services.user_service import UserService

router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(require_roles([UserRole.TEST_SCORER]))
    ],
    tags=["Users"]
)

@router.get(
    "/users/{user_id}",
    response_model=GetUserInfoResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_info(
        user_id: UUID,
        user_service: Annotated[UserService, Depends()]
):
    user_infos = await user_service.get_user_info_by_id(user_id=user_id)
    return user_infos

@router.get(
    "/users/",
    response_model=list[ListUsersResponse],
    status_code=status.HTTP_200_OK
)
async def list_users(user_service: Annotated[UserService, Depends()]):
    user_ids = await user_service.list_users()
    return user_ids
