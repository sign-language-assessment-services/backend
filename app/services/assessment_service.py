import logging
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models.assessment import Assessment
from app.database.tables.assessments import DbAssessment
from app.database.tables.assessments_tasks import DbAssessmentsTasks
from app.database.tables.tasks import DbTask
from app.mappers.assessment_mapper import assessment_to_domain
from app.repositories.assessments import get_assessment, list_assessments
from app.repositories.utils import add_entry
from app.services.exceptions.not_found import AssessmentNotFoundException, TaskNotFoundException
from app.services.task_service import TaskService

logger = logging.getLogger(__name__)


class AssessmentService:
    def __init__(self, task_service: Annotated[TaskService, Depends()]) -> None:
        self.task_service = task_service

    @staticmethod
    def create_assessment(session: Session, name: str, task_ids: list[UUID] = None) -> Assessment:
        db_assessment = DbAssessment(name=name)
        if task_ids:
            for position, task_id in enumerate(task_ids, start=1):
                db_task = session.get(DbTask, task_id)
                if db_task:
                    db_assessment.tasks_link.append(
                        DbAssessmentsTasks(position=position, task=db_task)
                    )
                else:
                    raise TaskNotFoundException(f"Task with id '{task_id}' not found.")

        add_entry(session=session, db=db_assessment)
        return assessment_to_domain(db_assessment)

    @staticmethod
    def get_assessment_by_id(session: Session, assessment_id: UUID) -> Assessment | None:
        if result := get_assessment(session=session, _id=assessment_id):
            return result
        raise AssessmentNotFoundException(f"Assessment with id '{assessment_id}' not found.")

    @staticmethod
    def list_assessments(session: Session) -> list[Assessment]:
        logger.info("Receive all assessments.")
        return list_assessments(session=session)
