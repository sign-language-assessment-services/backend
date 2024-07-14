from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


class DbExercise(Base):
    # pylint: disable=duplicate-code
    __tablename__ = "exercises"

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False
    )
    multimedia_file_id: Mapped[str] = mapped_column(
        ForeignKey("multimedia_files.id"),
        nullable=False
    )

    UniqueConstraint("position", "assessment_id")
