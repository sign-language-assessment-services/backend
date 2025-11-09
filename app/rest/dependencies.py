from typing import Annotated, Iterable

from fastapi import Depends, HTTPException, status

from app.core.models.role import UserRole
from app.core.models.user import User
from app.external_services.keycloak.auth_bearer import JWTBearer


async def get_current_user(user: Annotated[User, Depends(JWTBearer())]) -> User:
    return user


def require_roles(required: Iterable[UserRole]):
    async def _checker(current_user: Annotated[User, Depends(get_current_user)]):
        if not {r.value for r in required}.issubset({r.value for r in current_user.roles}):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The current user is not allowed to access this resource."
            )
        return True
    return _checker
