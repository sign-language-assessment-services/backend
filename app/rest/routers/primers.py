from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization.auth_bearer import JWTBearer
from app.core.models.primer import Primer, PrimerResponse
from app.core.models.user import User
from app.database.orm import get_db_session
from app.rest.dependencies import get_current_user
from app.services.primer_service import PrimerService

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.get("/primers/{primer_id}", response_model=PrimerResponse)
async def get_primer(
        primer_id: UUID,
        primer_service: Annotated[PrimerService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> Primer:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    primer = primer_service.get_primer_by_id(db_session, primer_id)
    if not primer:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return primer


@router.get("/primers/", response_model=list[PrimerResponse])
async def list_primers(
        primer_service: Annotated[PrimerService, Depends()],
        current_user: Annotated[User, Depends(get_current_user)],
        db_session: Session = Depends(get_db_session)
) -> list[Primer]:
    if "slas-frontend-user" not in current_user.roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return primer_service.list_primers(db_session)
