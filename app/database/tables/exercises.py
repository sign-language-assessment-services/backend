from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


class DbExercise(Base):
    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

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
