from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Submission:
    id: str
    user_id: str
    assessment_id: str
    answers: dict
    points: int
    maximum_points: int
    percentage: float
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
