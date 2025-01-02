from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization.auth_bearer import JWTBearer
from app.core.models.exercise import Exercise
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.services.exercise_service import ExerciseService

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.get("/exercises/{exercise_id}")
async def get_exercise(
        exercise_id: UUID,
        exercise_service: Annotated[ExerciseService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> Exercise:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    exercise = exercise_service.get_exercise_by_id(db_session, exercise_id)
    if not exercise:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return exercise


@router.get("/exercises/")
async def list_exercises(
        exercise_service: Annotated[ExerciseService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[Exercise]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return exercise_service.list_exercises(db_session)
