from typing import Dict, List

from fastapi import APIRouter

from app.core.interactors.assessments import (
    get_assessment_by_id,
    score_assessment
)

router = APIRouter()


@router.get("/assessments/{assessment_id}")
async def read_assessment(assessment_id: int):
    return get_assessment_by_id(assessment_id)


@router.post("/assessments/{assessment_id}/submissions/")
async def process_submission(
        assessment_id: int,
        submission: Dict[int, List[int]]
):
    return score_assessment(assessment_id, submission)
