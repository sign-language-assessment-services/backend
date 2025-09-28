import logging

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

logger = logging.getLogger(__name__)


class DatabaseSessionmaker:
    def __init__(self, engine: AsyncEngine, settings: BaseSettings) -> None:
        self.db_engine = engine
        self.expire_on_commit = settings.db_expire_on_commit
        self.autoflush = settings.db_autoflush

        self._cached_sessionmaker: async_sessionmaker | None = None

    def create_sessionmaker(self) -> None:
        sessionmaker = async_sessionmaker(
            bind=self.db_engine,
            expire_on_commit=self.expire_on_commit,
            autoflush=self.autoflush,
            class_=AsyncSession
        )
        logger.info(
            "Database sessionmaker %(_id)s created with: %(settings)s.",
            {
                "_id": id(sessionmaker),
                "settings": str(
                    {
                        "expire_on_commit": self.expire_on_commit,
                        "autoflush": self.autoflush
                    }
                )
            }
        )
        self._cached_sessionmaker = sessionmaker

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        if self._cached_sessionmaker is None:
            self.create_sessionmaker()
        else:
            logger.info(
                "Re-use existing database sessionmaker %(_id)s.",
                {"_id": id(self._cached_sessionmaker)}
            )
        return self._cached_sessionmaker
