import os
import logging
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

# Set the DB_URL environment variable before importing the app and database modules
os.environ['DB_URL'] = 'postgresql://test:test@localhost:5432/test'

from app.main import app
from app.pg import connect_to_db, disconnect_from_db, database

client = TestClient(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function", autouse=True)
async def setup_database(monkeypatch):
    logger.info("Setting up the database for testing")
    # Mock the DB_URL environment variable
    monkeypatch.setenv('DB_URL', 'postgresql://test:test@localhost:5432/test')
    await connect_to_db()
    yield
    await disconnect_from_db()

@pytest.fixture(scope="function")
def mock_database(monkeypatch):
    mock_db = AsyncMock()
    monkeypatch.setattr(database, "fetch_all", mock_db.fetch_all)
    return mock_db

@pytest.mark.asyncio
async def test_read_root_200(mock_database):
    # Mock the database fetch_all method
    mock_database.fetch_all.return_value = [{"message": "Hello, World!"}]

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

@pytest.mark.asyncio
async def test_read_root_500(mock_database):
    # Simulate a database error by raising an exception
    mock_database.fetch_all.side_effect = Exception("Database error")

    response = client.get("/")
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching messages"}