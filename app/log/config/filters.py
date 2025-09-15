import logging


# pylint: disable=too-few-public-methods
class HealthCheckFilter(logging.Filter):
    """Filter out health check requests from uvicorn access"""
    def filter(self, record: logging.LogRecord) -> bool:
        return "/health" not in record.getMessage()


# pylint: disable=too-few-public-methods
class WarningsAndBelowFilter(logging.Filter):
    """Filter to get only logs with level below WARNING

    This is necessary to avoid getting the same log message twice,
    where both handlers, i.e. stdout log handler and stderr log handler
    are defined. Therefore, stdout log handler should never log records
    of logging level ERROR or higher.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.ERROR
