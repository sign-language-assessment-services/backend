from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.rest.main as main_module
from app.rest.main import lifespan, run_migrations


@patch.object(main_module, run_migrations.__name__)
def test_lifespan(run_migration_mock) -> None:
    app = FastAPI(lifespan=lifespan)

    run_migration_mock.assert_not_called()
    with TestClient(app):
        run_migration_mock.assert_called_once_with()
