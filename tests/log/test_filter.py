import logging

import pytest

from app.log.config.filters import HealthCheckFilter, WarningsAndBelowFilter


@pytest.mark.parametrize(
    "message, expected",
    [
        ("GET /health HTTP/1.1", False),
        ("POST /api/v1/users HTTP/1.1", True)
    ]
)
def test_healthcheck_filter_behavior(message: str, expected: bool) -> None:
    log_filter = HealthCheckFilter()
    record = logging.LogRecord(
        name="healthcheck_filter_log",
        level=logging.DEBUG,
        pathname=__file__,
        lineno=10,
        msg=message,
        args=(),
        exc_info=None,
    )

    assert log_filter.filter(record) is expected


@pytest.mark.parametrize(
    "message, level, expected",
    [
        ("DEBUG", logging.DEBUG, True),
        ("INFO", logging.INFO, True),
        ("WARNING", logging.WARNING, True),
        ("ERROR", logging.ERROR, False),
        ("CRITICAL", logging.CRITICAL, False)
    ]
)
def test_warnings_and_below_filter_behavior(message: str, level: int, expected: bool) -> None:
    log_filter = WarningsAndBelowFilter()
    record = logging.LogRecord(
        name="warning_and_below_filter_log",
        level=level,
        pathname=__file__,
        lineno=10,
        msg=message,
        args=(),
        exc_info=None,
    )

    assert log_filter.filter(record) is expected
