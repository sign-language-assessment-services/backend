from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


class DbChoice(Base):
    __tablename__ = "choices"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    exercise_id: Mapped[str] = mapped_column(
        ForeignKey("exercises.id"),
        nullable=False
    )
    multimedia_file_id: Mapped[str] = mapped_column(
        ForeignKey("multimedia_files.id"),
        nullable=False
    )

    UniqueConstraint("exercise_id", "multimedia_file_id")
