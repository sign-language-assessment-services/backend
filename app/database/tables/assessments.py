from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.type_hints import Tasks


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
    tasks: Mapped[Tasks] = relationship(
        secondary="tasks_assessments",
        back_populates="assessments",
    )
