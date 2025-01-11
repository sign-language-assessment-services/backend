from uuid import UUID

from pydantic import BaseModel


class ScoreResponse(BaseModel):
    assessment_id: UUID
    user_id: UUID
    points: int
