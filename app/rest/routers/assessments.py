from fastapi import APIRouter

from app.core.interactors.assessments import get_assessment

router = APIRouter()


@router.get("/assessments/{assessment_id}")
async def read_assessment(assessment_id: int):  # pylint: disable=W0613
    return get_assessment()


@router.post("/assessments/{assessment_id}/submissions/")
async def process_submission(assessment_id: int):
    return {"passed": True}
