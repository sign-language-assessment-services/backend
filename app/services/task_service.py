from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer
from app.repositories.tasks import get_task
from app.services.exceptions.not_found import TaskNotFoundException


class TaskService:
    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID) -> Primer | Exercise | None:
        if result := get_task(session=session, _id=task_id):
            return result
        raise TaskNotFoundException(f"Task with id '{task_id}' not found.")
