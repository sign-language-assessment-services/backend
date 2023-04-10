from typing import Any

import pytest

from app.utils import strtobool


@pytest.mark.parametrize("val", ["y", "yes", "t", "true", "on", "1"])
def test_strtobool_returns_true(val: str) -> None:
    assert strtobool(val) is True


@pytest.mark.parametrize("val", ["n", "no", "f", "false", "off", "0"])
def test_strtobool_returns_false(val: str) -> None:
    assert strtobool(val) is False


@pytest.mark.parametrize("val", ["foo", None, [1, 2, 3], len, ...])
def test_strtobool_returns_default(val: Any) -> None:
    assert strtobool(val) is False
    assert strtobool(val, default=True) is True
