from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.tasks import DbTask


class DbPrimer(DbTask):
    __tablename__ = "primers"

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    bucket_object_id: Mapped[UUID] = mapped_column(
        ForeignKey("bucket_objects.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    bucket_object: Mapped["DbBucketObjects"] = relationship(
        back_populates="primers"
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "primer"
    }
