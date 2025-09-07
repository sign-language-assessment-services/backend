from unittest.mock import Mock

import pytest


@pytest.fixture
def settings() -> Mock:
    settings = Mock()
    settings.data_endpoint = "127.0.0.1:4242"
    settings.data_bucket_name = "testbucket"
    settings.data_root_user = "testuser"
    settings.data_root_password = "testpassword"
    settings.data_secure = False
    settings.db_user = "testuser"
    settings.db_password = "testpassword"
    settings.db_host = "localhost"
    return settings
