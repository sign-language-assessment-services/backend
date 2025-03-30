from uuid import UUID

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.database.tables.base import DbBase


class DbAssessmentsTasks(DbBase):
    __tablename__ = "assessments_tasks"

    @declared_attr
    def id(cls):  # pylint: disable=no-self-argument
        return None

    @declared_attr
    def created_at(cls):  # pylint: disable=no-self-argument
        return None

    # COLUMNS
    # ------------------------------------------------------------------------
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    # FOREIGN COLUMNS
    # ------------------------------------------------------------------------
    assessment_id: Mapped[UUID] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"),
        primary_key=True
    )
    task_id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        UniqueConstraint("assessment_id", "position"),
    )
