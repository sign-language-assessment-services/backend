from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class AssessmentSubmissionPick(StrEnum):
    LATEST = "latest"
    BEST = "best"


class AssessmentSubmissionFilter(BaseModel):
    user_id: UUID | None = Field(
        default=None,
        examples=[
            "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        ],
        description=(
            "Filter by user_id. Taking an user id from another user is only "
            "allowed for role 'test-scorer'."
        )
    )
    pick: AssessmentSubmissionPick | None = Field(
        default=None,
        examples=[
            AssessmentSubmissionPick.LATEST.value,
            AssessmentSubmissionPick.BEST.value
        ],
        description="Pick only the latest or best assessment submission."
    )

    model_config = {"extra": "forbid"}
