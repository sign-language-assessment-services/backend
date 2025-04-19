from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbTask(DbBase):
    __tablename__ = "tasks"

    # COLUMNS
    # ------------------------------------------------------------------------
    task_type: Mapped[str] = mapped_column(
        String(length=8),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    assessments: Mapped[list["DbAssessment"]] = relationship(
        secondary="assessments_tasks",
        back_populates="tasks"
    )
    assessment_links: Mapped[list["DbAssessmentsTasks"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan"
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_on": "task_type",
        "polymorphic_identity": "task"
    }
