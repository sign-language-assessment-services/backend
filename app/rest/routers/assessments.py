from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization.auth_bearer import JWTBearer
from app.core.models.assessment import Assessment, AssessmentResponse
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.services.assessment_service import AssessmentService

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
        assessment_id: UUID,
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> Assessment:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    assessment = assessment_service.get_assessment_by_id(db_session, assessment_id)
    if not assessment:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return assessment


@router.get("/assessments/", response_model=list[AssessmentResponse])
async def list_assessments(
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[Assessment]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.list_assessments(db_session)
