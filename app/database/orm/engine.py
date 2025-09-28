import logging

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

logger = logging.getLogger(__name__)


class DatabaseEngine:
    def __init__(self, settings: BaseSettings) -> None:
        # connection settings
        self.template = "{type}+{driver}://{user}:{pw}@{host}:{port}/{db}"
        self.type = settings.db_type
        self.driver = settings.db_driver
        self.host = settings.db_host
        self.port = settings.db_port
        self.user = settings.db_user
        self.password = settings.db_password
        self.db_name = settings.db_name

        # configuration settings
        self.pool_size = settings.db_pool_size
        self.pool_timeout = settings.db_pool_timeout
        self.pool_recycle = settings.db_pool_recycle
        self.pool_pre_ping = settings.db_pool_pre_ping
        self.max_overflow = settings.db_max_overflow

        self._cached_engine: AsyncEngine | None = None

    @property
    def connection_url(self) -> str:
        database_url = self.template.format(
            type=self.type,
            driver=self.driver,
            user=self.user,
            pw=self.password,
            host=self.host,
            port=self.port,
            db=self.db_name
        )
        return database_url

    @property
    def connection_url_password_masked(self) -> str:
        database_url = self.connection_url
        database_url.replace(self.password, "*" * len(self.password))
        return database_url

    def create_engine(self) -> None:
        db_engine = create_async_engine(
            url=self.connection_url,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
            pool_pre_ping=self.pool_pre_ping
        )
        logger.info(
            "Database engine %(url)s created with: %(settings)s.",
            {
                "url": self.connection_url_password_masked,
                "settings": str(
                    {
                        "pool_size": self.pool_size,
                        "max_overflow": self.max_overflow,
                        "pool_timeout": self.pool_timeout,
                        "pool_recycle": self.pool_recycle,
                        "pool_pre_ping": self.pool_pre_ping
                    }
                )
            }
        )
        self._cached_engine = db_engine

    @property
    def engine(self) -> AsyncEngine:
        if self._cached_engine is None:
            self.create_engine()
        else:
            logger.info(
                "Re-use existing database engine %(url)s.",
                {"url": self.connection_url_password_masked}
            )
        return self._cached_engine
