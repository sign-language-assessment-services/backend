from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.models.user import User
from app.database.orm import get_db_session
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.rest.dependencies import get_current_user
from app.rest.requests.exercises import CreateExerciseRequest
from app.rest.responses.exercises import (
    CreateExerciseResponse, GetExerciseResponse, ListExerciseResponse
)
from app.services.exercise_service import ExerciseService

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.post(
    "/exercises/",
    response_model=CreateExerciseResponse,
    status_code=status.HTTP_200_OK
)
async def create_exercise(
        exercise_data: CreateExerciseRequest,
        exercise_service: Annotated[ExerciseService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

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
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    exercise = exercise_service.get_exercise_by_id(
        session=db_session,
        exercise_id=exercise_id
    )
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The exercise id '{exercise_id}' was not found."
        )
    return exercise


@router.get(
    "/exercises/",
    response_model=list[ListExerciseResponse],
    status_code=status.HTTP_200_OK
)
async def list_exercises(
        exercise_service: Annotated[ExerciseService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
):
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user is not allowed to access this resource."
        )

    return exercise_service.list_exercises(db_session)
