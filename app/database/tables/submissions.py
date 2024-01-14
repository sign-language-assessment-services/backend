from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


# TODO: 1. new database creation
#       2. alembic / make database migration possible (after other todos listed here)
#
# TODO: code changes to reflect db changes
#       1. Use submissions_choices n:m table instead of answers column JSON
#       2. Create mappings Domain models <-> Database models


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    user_id: Mapped[str] = mapped_column(
        String(length=36),
        nullable=False
    )
    points: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    maximum_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False
    )
