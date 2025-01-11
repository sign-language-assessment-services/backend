from uuid import UUID

from pydantic import BaseModel


class Score(BaseModel):
    assessment_id: UUID
    user_id: UUID
    points: int
