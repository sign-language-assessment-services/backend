from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbChoice(DbBase):
    __tablename__ = "choices"

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    bucket_object_id: Mapped[UUID] = mapped_column(
        ForeignKey("bucket_objects.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    bucket_object: Mapped["DbBucketObjects"] = relationship(
        back_populates="choices"
    )
    multiple_choices: Mapped[list["DbMultipleChoice"]] = relationship(
        secondary="multiple_choices_choices",
        back_populates="choices",
        viewonly=True
    )
    associations: Mapped[list["DbMultipleChoicesChoices"]] = relationship(
        back_populates="choice",
        passive_deletes=True
    )
