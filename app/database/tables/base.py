from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DbBase(DeclarativeBase):
    # COLUMNS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        sort_order=-3  # should be the first column on table creation
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        sort_order=-2  # should be the second column on table creation
    )
    modified_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=text("now()"),
        sort_order=-1  # should be third column on table creation
    )


    def __repr__(self) -> str:
        attr = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"<{self.__class__.__name__}[{id(self)}] ({attr})>"
