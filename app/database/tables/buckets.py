from sqlalchemy import Enum, String, Unicode, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.media_types import MediaType
from app.database.tables.base import DbBase
from app.database.type_hints import Choices, Primers


class DbBucket(DbBase):
    __tablename__ = "buckets"

    # COLUMNS
    # ------------------------------------------------------------------------
    bucket: Mapped[str] = mapped_column(
        String(length=63),
        nullable=False
    )
    key: Mapped[str] = mapped_column(
        Unicode(length=1024),
        nullable=False
    )
    mediatype: Mapped[MediaType] = mapped_column(
        Enum(MediaType),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    primers: Mapped[Primers] = relationship(
        back_populates="buckets"
    )
    choices: Mapped[Choices] = relationship(
        back_populates="buckets"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("bucket", "key")
