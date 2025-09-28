from uuid import uuid4

import pytest

from app.core.models.user import User
from app.dependencies import get_current_user


@pytest.mark.asyncio
async def test_get_current_user() -> None:
    user = User(id=uuid4(), roles=[])
    result = await get_current_user(user)
    assert result == user
