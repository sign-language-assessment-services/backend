from unittest.mock import Mock

import pytest


@pytest.fixture
def settings() -> Mock:
    settings = Mock()
    settings.data_endpoint = "127.0.0.1:4242"
    settings.data_bucket_name = "testbucket"
    settings.data_secure = False
    settings.db_user = "testuser"
    settings.db_password = "testpassword"
    settings.db_host = "localhost"
    settings.data_sts_endpoint = "http://127.0.0.1:4242"
    return settings
