from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.exercise import Exercise
from app.core.models.primer import Primer
from app.repositories.tasks import get_task


class TaskService:
    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID) -> Primer | Exercise | None:
        task = get_task(session=session, _id=task_id)
        return task
