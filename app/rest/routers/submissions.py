from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.models.submission import Submission
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.rest.routers.assessments import router
from app.services.assessment_service import AssessmentService


@router.get("/submissions/")
async def list_submissions(
        # user_id: str,
        assessment_service: Annotated[AssessmentService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[Submission]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    # if current_user.id != user_id and "test-scorer" not in current_user.roles:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN)

    return assessment_service.list_submissions(session=db_session)
