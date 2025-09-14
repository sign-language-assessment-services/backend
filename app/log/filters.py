import logging
from logging import LogRecord


# pylint: disable=too-few-public-methods
class HealthCheckFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        return "/health" not in record.getMessage()
