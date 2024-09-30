from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.type_hints import Answers


@dataclass
class Submission:
    user_id: str
    assessment_id: str
    answers: Answers
    points: int
    maximum_points: int
    percentage: float

    id: UUID = field(default_factory=lambda: uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
