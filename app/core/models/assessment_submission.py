from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AssessmentSubmission(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime | None = Field(default=None)

    user_id: UUID
    assessment_id: UUID
    score: float | None = None
    finished: bool = Field(default=False)
    finished_at: datetime | None = None
