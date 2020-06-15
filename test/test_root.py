"""Tests for root '/' endpoint"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    """Test Read access for endpoint '/'"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World!"}
