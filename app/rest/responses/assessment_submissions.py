from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AssessmentSubmissionResponse(BaseModel):
    id: UUID
    user_id: UUID
    assessment_id: UUID
    score: float | None
    finished_at: datetime | None


class AssessmentSubmissionListResponse(BaseModel):
    id: UUID
