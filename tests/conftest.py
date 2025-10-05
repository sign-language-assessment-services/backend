import pytest

from tests.settings_for_tests import TestSettings


@pytest.fixture(scope="session")
def settings() -> TestSettings:
    return TestSettings()
