import logging


# pylint: disable=too-few-public-methods
class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "/health" not in record.getMessage()
