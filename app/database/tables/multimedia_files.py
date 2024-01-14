from datetime import datetime

from sqlalchemy import String, TIMESTAMP, Unicode, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.tables.base import Base


class MultiMediaFiles(Base):
    __tablename__ = "multimedia_files"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    bucket: Mapped[str] = mapped_column(
        String(length=63),
        nullable=False
    )
    key: Mapped[str] = mapped_column(
        Unicode(length=1024),
        nullable=False
    )

    UniqueConstraint("bucket", "key")
