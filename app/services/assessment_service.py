from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.assessment import Assessment
from app.external_services.minio.client import ObjectStorageClient
from app.repositories.assessments import add_assessment, get_assessment, list_assessments
from app.settings import get_settings


class AssessmentService:
    def __init__(
            self,
            object_storage_client: Annotated[ObjectStorageClient, Depends()],
            settings: Annotated[Settings, Depends(get_settings)],
    ):
        self.object_storage_client = object_storage_client
        self.settings = settings

    @staticmethod
    def create_assessment(session: Session, name: str) -> Assessment:
        assessment = Assessment(name=name)
        add_assessment(session=session, assessment=assessment)
        return assessment

    @staticmethod
    def get_assessment_by_id(session: Session, assessment_id: UUID) -> Assessment | None:
        return get_assessment(session=session, _id=assessment_id)

    @staticmethod
    def list_assessments(session: Session) -> list[Assessment]:
        return list_assessments(session=session)
