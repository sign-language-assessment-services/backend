import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import User
from app.dependencies import get_current_user, get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.requests.assessments import CreateAssessmentRequest
from app.rest.responses.assessments import (
    CreateAssessmentResponse, GetAssessmentResponse, ListAssessmentResponse
)
from app.services.assessment_service import AssessmentService

logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[Depends(JWTBearer())],
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
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

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
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    assessment = await assessment_service.get_assessment_by_id(
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
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: AsyncSession = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    logger.info("List assessments requested.")
    assessments = await assessment_service.list_assessments(session=db_session)
    return assessments
