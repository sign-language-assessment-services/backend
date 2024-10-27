from pydantic import BaseModel


class AssessmentSummary(BaseModel):
    name: str
