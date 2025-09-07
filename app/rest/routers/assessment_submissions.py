from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.models.user import User
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import get_current_user
from app.rest.requests.assessment_submissions import UpdateAssessmentSubmissionToFinishedRequest
from app.rest.responses.assessment_submissions import (
    CreateAssessmentSubmissionResponse, GetAssessmentSubmissionResponse,
    ListAssessmentSubmissionResponse, UpdateAssessmentSubmissionToFinishedResponse
)
from app.services.assessment_submission_service import AssessmentSubmissionService

router = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["Assessment Submissions"]
)


@router.post(
    "/assessments/{assessment_id}/submissions/",
    response_model=CreateAssessmentSubmissionResponse,
    status_code=status.HTTP_200_OK
)
async def create_assessment_submission(
        assessment_id: UUID,
        submission_service: Annotated[AssessmentSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session),
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    assessment_submission = submission_service.create_assessment_submission(
        session=db_session,
        user_id=current_user.id,
        assessment_id=assessment_id
    )
    return assessment_submission


@router.get(
    "/assessment_submissions/{submission_id}",
    response_model=GetAssessmentSubmissionResponse,
    status_code=status.HTTP_200_OK
)
async def get_assessment_submission(
        submission_id: UUID,
        submission_service: Annotated[AssessmentSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    submission = submission_service.get_assessment_submission_by_id(
        session=db_session,
        submission_id=submission_id
    )
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The assessment submission id '{submission_id}' was not found."
        )
    return submission


@router.get(
    "/assessment_submissions/",
    response_model=list[ListAssessmentSubmissionResponse],
    status_code=status.HTTP_200_OK
)
async def list_submissions(
        assessment_submission_service: Annotated[AssessmentSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    submissions = assessment_submission_service.list_assessment_submissions(session=db_session)
    return submissions


@router.put(
    "/assessment_submissions/{assessment_submission_id}",
    response_model=UpdateAssessmentSubmissionToFinishedResponse,
    status_code=status.HTTP_200_OK
)
async def update_assessment_submission(
        # this update endpoint handles only setting the assessment submission to finished,
        # but this behavior can easily be changed by modifying/replacing the request model
        # for broader use cases. At the time of writing this, only this use case was needed.
        assessment_submission_id: UUID,
        data: UpdateAssessmentSubmissionToFinishedRequest,
        submission_service: Annotated[AssessmentSubmissionService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    submission = submission_service.get_assessment_submission_by_id(
        session=db_session,
        submission_id=assessment_submission_id
    )
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The assessment submission id '{assessment_submission_id}' was not found."
        )

    update_dict = data.model_dump(exclude_unset=True, exclude_none=True)
    updated_submission = submission_service.update_assessment_submission(
        session=db_session,
        submission_id=assessment_submission_id,
        **update_dict
    )
    return updated_submission
