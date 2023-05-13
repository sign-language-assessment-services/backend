from typing import Annotated

from fastapi import Depends

from app.core.models.assessment import Assessment
from app.services.assessment_service import AssessmentService


def get_assessment_by_id(
        assessment_id: int,
        assessment_service: Annotated[AssessmentService, Depends()]
) -> Assessment:
    return assessment_service.get_assessment_by_id(assessment_id)


def score_assessment(
        assessment_id: int,
        submission: dict[int, list[int]],
        assessment_service: Annotated[AssessmentService, Depends()]
) -> dict[str, int]:
    assessment = assessment_service.get_assessment_by_id(assessment_id)
    return assessment.score(submission)
