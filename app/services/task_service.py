from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.task import Task
from app.repositories.tasks import get_task, list_tasks
from app.settings import get_settings


class TaskService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID) -> Task | None:
        return get_task(session=session, _id=task_id)

    @staticmethod
    def list_tasks(session: Session) -> list[Task]:
        return list_tasks(session=session)
