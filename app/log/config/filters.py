import logging


# pylint: disable=too-few-public-methods
class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/health" not in record.getMessage()


# pylint: disable=too-few-public-methods
class WarningsAndBelowFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.WARNING
