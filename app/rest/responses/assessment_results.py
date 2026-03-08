from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExerciseScoreResponse(BaseModel):
    exercise_id: UUID
    score: float | None


class AssessmentSubmissionResultResponse(BaseModel):
    assessment_submission_id: UUID
    user_id: UUID
    exercise_scores: list[ExerciseScoreResponse]
    total_score: float | None
    finished_at: datetime


class AssessmentResultResponse(BaseModel):
    submissions: list[AssessmentSubmissionResultResponse]
