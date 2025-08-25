from typing import Annotated

from fastapi import Depends

from app.core.models.user import User
from app.external_services.keycloak.auth_bearer import JWTBearer


async def get_current_user(user: Annotated[User, Depends(JWTBearer())]) -> User:
    return user
