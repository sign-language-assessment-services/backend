import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.models.role import UserRole
from app.core.models.user import User
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import get_current_user, require_roles
from app.rest.filters.assessment_submissions import AssessmentSubmissionFilter
from app.rest.requests.assessment_submissions import UpdateAssessmentSubmissionToFinishedRequest
from app.rest.responses.assessment_submissions import (
    CreateAssessmentSubmissionResponse, GetAssessmentSubmissionResponse,
    ListAssessmentSubmissionResponse, UpdateAssessmentSubmissionToFinishedResponse
)
from app.services.assessment_submission_service import AssessmentSubmissionService

logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(require_roles([UserRole.FRONTEND]))
    ],
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
        db_session: Annotated[Session, Depends(get_db_session)]
):
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
        db_session: Annotated[Session, Depends(get_db_session)]
):
    logger.info("Get assessment submission requested.")
    submission = submission_service.get_assessment_submission_by_id(
        session=db_session,
        submission_id=submission_id
    )
    return submission


@router.get(
    "/assessment_submissions/",
    response_model=list[ListAssessmentSubmissionResponse],
    status_code=status.HTTP_200_OK
)
async def list_submissions(
        assessment_submission_service: Annotated[AssessmentSubmissionService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)],
        current_user: Annotated[User, Depends(get_current_user)],
        filter_query: Annotated[AssessmentSubmissionFilter, Query()]
):
    allowed_roles_user_id_filter = [UserRole.TEST_SCORER]
    if (
        filter_query.user_id and filter_query.user_id != current_user.id and
        not any(r in allowed_roles_user_id_filter for r in current_user.roles)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view submissions for another user."
        )

    # The user_id is always the current user id, except for an eligible role to
    # filter for user ids, like a 'test-scorer'.
    user_id = current_user.id
    if any(r in allowed_roles_user_id_filter for r in current_user.roles):
        user_id = filter_query.user_id

    submissions = assessment_submission_service.list_assessment_submissions(
        session=db_session,
        user_id=user_id,
        pick_strategy=filter_query.pick
    )
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
        db_session: Annotated[Session, Depends(get_db_session)]
):
    logger.info("Update assessment submission requested.")
    # TODO: The call to get the assessment submission beforehand checks
    #       if a submission for this id exists and an exception is raised if
    #       the assessment submission does not exist. This is not necessary.
    #       Another way is to drill down to the database call and let an error
    #       be raised if the assessment submission does not exist in the db.
    #       (maybe there is already an error raised, but which error exactly?)
    #       This can be reraised as AssessmentSubmissionNotFoundException in
    #       the service layer, so that the global exception handler will
    #       respond with 404. There is also the case that after the update the
    #       assessment submission is requested again with the same id in the
    #       underlying service layer. This should be replaced by the database
    #       respond to the SQLAlchemy update execution.
    submission_service.get_assessment_submission_by_id(
        session=db_session,
        submission_id=assessment_submission_id
    )  # raises exception if assessment submission does not exist (replace me)

    update_dict = data.model_dump(exclude_unset=True, exclude_none=True)
    updated_submission = submission_service.update_assessment_submission(
        session=db_session,
        submission_id=assessment_submission_id,
        **update_dict
    )
    return updated_submission
