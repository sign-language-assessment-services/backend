import logging
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.repositories.assessments import add_assessment, get_assessment, list_assessments
from app.services.task_service import TaskService

logger = logging.getLogger(__name__)


class AssessmentService:
    def __init__(self, task_service: Annotated[TaskService, Depends()]) -> None:
        self.task_service = task_service

    def create_assessment(self, session: Session, name: str, task_ids: list[UUID] = None) -> Assessment:
        assessment = Assessment(
            name=name,
            tasks=[
                self.task_service.get_task_by_id(session=session, task_id=task_id)
                for task_id in task_ids
            ] if task_ids else []
        )
        add_assessment(session=session, assessment=assessment)
        return assessment

    @staticmethod
    async def get_assessment_by_id(session: AsyncSession, assessment_id: UUID) -> Assessment | None:
        return await get_assessment(session=session, _id=assessment_id)

    @staticmethod
    async def list_assessments(session: AsyncSession) -> list[Assessment]:
        logger.info("Trying to receive all assessments.")
        return await list_assessments(session=session)
