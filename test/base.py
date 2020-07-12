from fastapi.testclient import TestClient

from app.main import app


def get_test_client():
    return TestClient(app)
