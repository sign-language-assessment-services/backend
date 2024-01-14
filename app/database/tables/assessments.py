from datetime import datetime

from sqlalchemy import String, TIMESTAMP, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        Unicode(length=100),
        nullable=False,
        unique=True
    )
