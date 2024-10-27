from pydantic import BaseModel, Field

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer


class Assessment(BaseModel):
    name: str
    items: list[Primer | Exercise] = Field(default_factory=list)
