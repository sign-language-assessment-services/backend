from uuid import uuid4

from app.core.models.user import User

test_taker_1 = User(
    id=uuid4(),
    roles=["slas-frontend-user", "test-taker"]
)

test_taker_2 = User(
    id=uuid4(),
    roles=["slas-frontend-user", "test-taker"]
)
