"""Unit tests for the Python Web App.

This module contains unit tests for the FastAPI application endpoints.
It mocks the database connection to isolate the API functionality from
the actual database interactions.
"""

import logging
import os
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

# Set the DB_URL environment variable before importing the app and database modules
os.environ["DB_URL"] = "postgresql://test:test@localhost:5432/test"
from app.main import app  # noqa: E402
from app.pg import connect_to_db, database, disconnect_from_db  # noqa: E402

client = TestClient(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function", autouse=True)
async def setup_database(monkeypatch):
    """Set up the database for testing.

    This fixture mocks the database connection for unit tests.

    Args:
        monkeypatch: Pytest fixture for patching objects
    """
    logger.info("Setting up the database for testing")
    # Mock the DB_URL environment variable
    monkeypatch.setenv("DB_URL", "postgresql://test:test@localhost:5432/test")
    await connect_to_db()
    yield
    await disconnect_from_db()


@pytest.fixture(scope="function")
def mock_database(monkeypatch):
    """Mock the database for testing.

    This fixture creates a mock for the database fetch_all method.

    Args:
        monkeypatch: Pytest fixture for patching objects

    Returns:
        AsyncMock: A mock object for the database
    """
    mock_db = AsyncMock()
    monkeypatch.setattr(database, "fetch_all", mock_db.fetch_all)
    return mock_db


@pytest.mark.asyncio
async def test_read_root_200(mock_database):
    """Test that the root endpoint returns a 200 status code with mocked data.

    Args:
        mock_database: Fixture that provides a mock database
    """
    # Mock the database fetch_all method
    mock_database.fetch_all.return_value = [{"message": "Hello, World!"}]

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


@pytest.mark.asyncio
async def test_read_root_500(mock_database):
    """Test that the root endpoint returns a 500 status code on database errors.

    Args:
        mock_database: Fixture that provides a mock database
    """
    # Simulate a database error by raising an exception
    mock_database.fetch_all.side_effect = Exception("Database error")

    response = client.get("/")
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching messages"}
