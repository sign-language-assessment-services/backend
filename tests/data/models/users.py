from uuid import UUID, uuid4

from app.core.models.role import UserRole
from app.core.models.user import User

test_taker_1 = User(
    # Use a fix uuid for better testing. Then test_taker_1 can be instantiated
    # multiple times, but the id will be the same.
    id=UUID("a78898c3-256f-4510-8bfd-0bf979a14e72"),
    roles=[UserRole.FRONTEND_ACCESS, UserRole.TEST_TAKER]
)

test_taker_2 = User(
    id=uuid4(),
    roles=[UserRole.FRONTEND_ACCESS, UserRole.TEST_TAKER]
)


test_scorer_1 = User(
    id=uuid4(),
    roles=[UserRole.FRONTEND_ACCESS, UserRole.TEST_SCORER]
)
