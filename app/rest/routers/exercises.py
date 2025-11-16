import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.models.role import UserRole
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import require_roles
from app.rest.requests.exercises import CreateExerciseRequest
from app.rest.responses.exercises import (
    CreateExerciseResponse, GetExerciseResponse, ListExerciseResponse
)
from app.services.exercise_service import ExerciseService

logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(require_roles([UserRole.FRONTEND]))
    ],
    tags=["Exercises"]
)


@router.post(
    "/exercises/",
    response_model=CreateExerciseResponse,
    status_code=status.HTTP_200_OK
)
async def create_exercise(
        exercise_data: CreateExerciseRequest,
        exercise_service: Annotated[ExerciseService, Depends()],
        db_session: Session = Depends(get_db_session)
):
    return exercise_service.create_exercise(
        session=db_session,
        points=1,  # currently each exercise has only one point
        multimedia_file_id=exercise_data.multimedia_file_id,
        multiple_choice_id=exercise_data.multiple_choice_id
    )


@router.get(
    "/exercises/{exercise_id}",
    response_model=GetExerciseResponse,
    status_code=status.HTTP_200_OK
)
async def get_exercise(
        exercise_id: UUID,
        exercise_service: Annotated[ExerciseService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    logger.info("Get exercise requested.")
    logger.debug(
        "Get exercise requested with session id %(session_id)s.",
        {"session_id": id(db_session)}
    )
    exercise = exercise_service.get_exercise_by_id(
        session=db_session,
        exercise_id=exercise_id
    )
    return exercise


@router.get(
    "/exercises/",
    response_model=list[ListExerciseResponse],
    status_code=status.HTTP_200_OK
)
async def list_exercises(
        exercise_service: Annotated[ExerciseService, Depends()],
        db_session: Annotated[Session, Depends(get_db_session)]
):
    exercises = exercise_service.list_exercises(db_session)
    return exercises
