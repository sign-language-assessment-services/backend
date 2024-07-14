from datetime import datetime

from sqlalchemy import String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True,
        sort_order=-2  # should be the first column on table creation
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        sort_order=-1  # should be the second column on table creation
    )

    def __repr__(self) -> str:
        attr = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"<{self.__class__.__name__}[{id(self)}] ({attr})>"
