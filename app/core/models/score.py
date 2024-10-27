from typing import Any

from pydantic import BaseModel, Field


class Score(BaseModel):
    points: int
    maximum_points: int
    percentage: float = Field(init=False, ge=0, le=100)

    def model_post_init(self, __context: Any) -> None:
        self.percentage = self.points / self.maximum_points * 100
