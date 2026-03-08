from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExerciseScore(BaseModel):
    exercise_id: UUID
    score: float | None


class SubmissionResult(BaseModel):
    assessment_submission_id: UUID
    user_id: UUID
    exercise_scores: list[ExerciseScore]
    total_score: float | None
    finished_at: datetime


class AssessmentResult(BaseModel):
    submissions: list[SubmissionResult]
