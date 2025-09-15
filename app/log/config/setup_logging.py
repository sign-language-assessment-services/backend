import json
import logging
import logging.config
from pathlib import Path


def setup_logging():
    path = Path(__file__).parent.absolute() / "config.json"
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    _configure_third_party_loggers()


def _configure_third_party_loggers():
    fastapi_logger = logging.getLogger("fastapi")

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")

    sqlalchemy_logger = logging.getLogger("sqlalchemy")
    sqlalchemy_engine_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_pool_logger = logging.getLogger("sqlalchemy.pool")
    sqlalchemy_orm_logger = logging.getLogger("sqlalchemy.orm")

    alembic_logger = logging.getLogger("alembic")

    for logger in (
        fastapi_logger,
        uvicorn_logger, uvicorn_error_logger, uvicorn_access_logger,
        sqlalchemy_logger, sqlalchemy_engine_logger, sqlalchemy_pool_logger, sqlalchemy_orm_logger,
        alembic_logger
    ):
        if logger.level == logging.NOTSET:
            logger.setLevel(logging.WARNING)
