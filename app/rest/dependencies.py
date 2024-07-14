from typing import Annotated

from fastapi import Depends

from app.authorization.auth_bearer import JWTBearer
from app.core.models.user import User


async def get_current_user(user: Annotated[User, Depends(JWTBearer())]) -> User:
    return user
