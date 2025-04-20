from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AssessmentSubmissionResponse(BaseModel):
    id: UUID
    user_id: UUID
    assessment_id: UUID
    score: float | None
    finished: bool = Field(default=False)
    finished_at: datetime | None


class AssessmentSubmissionCreatedResponse(BaseModel):
    id: UUID


class AssessmentSubmissionListResponse(BaseModel):
    id: UUID
