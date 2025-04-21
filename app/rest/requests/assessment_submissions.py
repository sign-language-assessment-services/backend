from pydantic import BaseModel


class AssessmentSubmissionUpdateFinishedRequest(BaseModel):
    finished: bool
