import pytest
import fastapi
from fastapi.testclient import TestClient
from unittest.mock import patch

from routers import router

app = fastapi.FastAPI()
app.include_router(router)

client = TestClient(app)


@pytest.fixture
def mock_send_message():
    with patch('routers.send_message') as mock:
        yield mock


def test_send_message(mock_send_message):
    message_data = {
        "room_id": 1,
        "content": "Hello, world!",
    }

    response = client.post("/message", json=message_data)

    assert response.status_code == 201

    mock_send_message.assert_called_once_with(room_id=1, content="Hello, world!")
