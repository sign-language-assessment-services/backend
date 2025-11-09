from enum import Enum

from pydantic import BaseModel, Field


class AssessmentSubmissionScope(str, Enum):
    MINE = "mine"
    ALL = "all"


class UpdateAssessmentSubmissionToFinishedRequest(BaseModel):
    finished: bool = Field(default=True)
