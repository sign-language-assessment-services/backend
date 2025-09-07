from pydantic import BaseModel, Field


class UpdateAssessmentSubmissionToFinishedRequest(BaseModel):
    finished: bool = Field(default=True)
