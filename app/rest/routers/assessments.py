from fastapi import APIRouter

from app.core.interactors.assessments import get_assessment_by_id

router = APIRouter()


@router.get("/assessments/{assessment_id}")
async def read_assessment(assessment_id: int):
    return get_assessment_by_id(assessment_id)


@router.post("/assessments/{assessment_id}/submissions/")
async def process_submission(assessment_id: int):  # pylint: disable=W0613
    return {"passed": True}
