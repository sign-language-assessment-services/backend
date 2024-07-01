import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Submission:
    user_id: str
    assessment_id: str
    answers: dict[str, dict[str, bool]]
    points: int
    maximum_points: int
    percentage: float

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
