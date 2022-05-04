from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


@pytest.mark.app
def test_index():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.app
def test_default():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Example!"}
