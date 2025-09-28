from typing import Annotated, AsyncGenerator

from fastapi import Depends
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.core.models.user import User
from app.database.orm.engine import DatabaseEngine
from app.database.orm.session import DatabaseSessionmaker, logger
from app.external_services.keycloak.auth_bearer import JWTBearer
from app.settings import get_settings


async def get_current_user(user: Annotated[User, Depends(JWTBearer())]) -> User:
    logger.info("Get authenticated user %(user_id)s.", {"user_id": user.id})
    return user


def get_db_engine(
        settings: Annotated[BaseSettings, Depends(get_settings)]
) -> AsyncEngine:
    db_engine_manager = DatabaseEngine(settings=settings)
    logger.info("Engine manager instantiated.")
    return db_engine_manager.engine


async def get_db_session(
        engine: Annotated[AsyncEngine, Depends(get_db_engine)],
        settings: Annotated[BaseSettings, Depends(get_settings)]
) -> AsyncGenerator[AsyncSession]:
    db_sessionmaker = DatabaseSessionmaker(engine=engine, settings=settings)
    logger.info("Sessionmaker instantiated.")
    async with db_sessionmaker.sessionmaker() as session:
        try:
            logger.info("Run database session %(_id)s.", {"_id": id(session)})
            yield session
            logger.info("End database session %(_id)s.", {"_id": id(session)})
        except Exception as exc:
            await session.rollback()
            logger.exception(exc)
            raise RuntimeError(f"Database session error: {exc!r}") from exc
