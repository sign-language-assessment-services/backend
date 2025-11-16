import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.models.role import UserRole
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import require_roles
from app.rest.requests.exercise_submissions import UpsertExerciseSubmissionRequest
from app.rest.responses.exercise_submissions import (
    GetExerciseSubmissionResponse, ListExerciseSubmissionResponse, UpsertExerciseSubmissionResponse
)
from app.services.exercise_submission_service import ExerciseSubmissionService

logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(require_roles([UserRole.FRONTEND]))
    ],
    tags=["Exercise Submissions"]
)


@router.get(
    "/exercise_submissions/{exercise_submission_id}",
    response_model=GetExerciseSubmissionResponse,
    status_code=status.HTTP_200_OK
)
async def get_submission(
        exercise_submission_id: UUID,
        submission_service: Annotated[ExerciseSubmissionService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    logger.info("Get exercise submission requested.")
    logger.debug(
        "Get exercise submission requested with session id %(session_id)s.",
        {"session_id": id(db_session)}
    )
    submission = submission_service.get_exercise_submission_by_id(
        session=db_session,
        submission_id=exercise_submission_id
    )
    return submission


@router.get(
    "/exercise_submissions/",
    response_model=list[ListExerciseSubmissionResponse],
    status_code=status.HTTP_200_OK
)
async def list_submissions(
        submission_service: Annotated[ExerciseSubmissionService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)],
        assessment_submission_id: UUID | None = None,
        exercise_id: UUID | None = None
):
    submissions = submission_service.list_exercise_submissions(
        session=db_session,
        assessment_submission_id=assessment_submission_id,
        exercise_id=exercise_id
    )
    return submissions


@router.post(
    "/assessment_submissions/{assessment_submission_id}/exercises/{exercise_id}/submissions/",
    response_model=UpsertExerciseSubmissionResponse,
    status_code=status.HTTP_200_OK
)
async def upsert_exercise_submission(
        assessment_submission_id: UUID,
        exercise_id: UUID,
        data: UpsertExerciseSubmissionRequest,
        exercise_submission_service: Annotated[ExerciseSubmissionService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    exercise_submission = exercise_submission_service.upsert_exercise_submission(
        session=db_session,
        data=data.model_dump(exclude_none=True),
        assessment_submission_id=assessment_submission_id,
        exercise_id=exercise_id
    )
    return exercise_submission
