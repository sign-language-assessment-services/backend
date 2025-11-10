import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.models.role import UserRole
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import require_roles
from app.rest.requests.assessments import CreateAssessmentRequest
from app.rest.responses.assessments import (
    CreateAssessmentResponse, GetAssessmentResponse, ListAssessmentResponse
)
from app.services.assessment_service import AssessmentService

logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(require_roles([UserRole.FRONTEND]))
    ],
    tags=["Assessments"]
)


@router.post(
    "/assessments/",
    response_model=CreateAssessmentResponse,
    status_code=status.HTTP_200_OK
)
async def create_assessment(
        data: CreateAssessmentRequest,
        assessment_service: Annotated[AssessmentService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    assessment = assessment_service.create_assessment(
        session=db_session,
        name=data.name,
        task_ids=data.tasks
    )
    return assessment


@router.get(
    "/assessments/{assessment_id}",
    response_model=GetAssessmentResponse,
    status_code=status.HTTP_200_OK
)
async def get_assessment(
        assessment_id: UUID,
        assessment_service: Annotated[AssessmentService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    assessment = assessment_service.get_assessment_by_id(
        session=db_session,
        assessment_id=assessment_id
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The assessment id '{assessment_id}' was not found."
        )
    return assessment


@router.get(
    "/assessments/",
    response_model=list[ListAssessmentResponse],
    status_code=status.HTTP_200_OK
)
async def list_assessments(
        assessment_service: Annotated[AssessmentService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    logger.info("List assessments requested.")
    assessments = assessment_service.list_assessments(session=db_session)
    return assessments
