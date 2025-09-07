from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateAssessmentSubmissionResponse(BaseModel):
    id: UUID


class GetAssessmentSubmissionResponse(BaseModel):
    id: UUID
    user_id: UUID
    assessment_id: UUID
    score: float | None
    finished: bool
    finished_at: datetime | None


class ListAssessmentSubmissionResponse(BaseModel):
    id: UUID
    assessment_id: UUID
    user_id: UUID


class UpdateAssessmentSubmissionToFinishedResponse(BaseModel):
    id: UUID
    finished: bool
    score: float
    finished_at: datetime
