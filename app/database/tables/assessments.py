from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.assessments_tasks import assessments_tasks
from app.database.tables.base import DbBase


class DbAssessment(DbBase):
    __tablename__ = "assessments"

    # COLUMNS
    # ------------------------------------------------------------------------
    name: Mapped[str] = mapped_column(
        Unicode(length=100),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    tasks: Mapped[list["DbTask"]] = relationship(
        secondary=assessments_tasks,
        back_populates="assessments"
    )
