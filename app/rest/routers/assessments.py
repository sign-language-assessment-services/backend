# pylint: disable=unused-argument

from typing import Any, Dict, List

from fastapi import APIRouter
from starlette.authentication import requires
from starlette.requests import Request

from app.core.interactors.assessments import get_assessment_by_id, score_assessment

router = APIRouter()


@router.get("/assessments/{assessment_id}")
@requires("slas-frontend-user")
async def read_assessment(assessment_id: int, request: Request) -> dict[str, Any]:
    return get_assessment_by_id(assessment_id)


@router.post("/assessments/{assessment_id}/submissions/")
@requires("test-taker")
async def process_submission(
        assessment_id: int,
        submission: Dict[int, List[int]],
        request: Request
) -> dict[str, int]:
    return score_assessment(assessment_id, submission)
