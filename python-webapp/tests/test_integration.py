"""Integration tests for the Python Web App.

This module contains integration tests that test the application with a real
PostgreSQL database using testcontainers. It verifies that the API endpoints
work correctly with database interactions.
"""

import logging
import os
import socket
import subprocess
import time

import pytest
from app.main import app  # noqa: E402
from app.pg import connect_to_db, database, disconnect_from_db  # noqa: E402
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_port_available(port):
    """Check if a port is available on localhost.

    Args:
        port: The port number to check

    Returns:
        bool: True if the port is available, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) != 0


def find_free_port():
    """Find a free port on localhost.

    Returns:
        int: An available port number
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


# Find an available port dynamically
PG_PORT = find_free_port()
logger.info(f"Using port {PG_PORT} for PostgreSQL container")

os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_DB"] = "test"
container = PostgresContainer("postgres:14").with_bind_ports(5432, PG_PORT)
container.start()
os.environ["DB_URL"] = container.get_connection_url()
DATABASE_URL = os.environ["DB_URL"]
logger.info("========> Postgres container started with DB_URL: %s", DATABASE_URL)
print(f"========> Postgres container started with DB_URL: {DATABASE_URL}")

# Use the container's connection URL for the application
os.environ["DB_URL"] = DATABASE_URL
logger.info("Updated DB_URL: %s", os.environ["DB_URL"])


@pytest.fixture(scope="session", autouse=True)
def postgres_container():
    """Pytest fixture that provides a PostgreSQL container.

    This fixture is automatically used for all tests in the session.
    It ensures the container is properly stopped after all tests are complete.

    Yields:
        PostgresContainer: The running PostgreSQL container
    """
    try:
        yield container
    finally:
        # Ensure container is stopped and removed even if tests fail
        try:
            logger.info("Stopping PostgreSQL container")
            container.stop()
            logger.info("PostgreSQL container stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping PostgreSQL container: {e}")


@pytest.fixture(scope="session")
async def setup_database():
    """Pytest fixture that sets up the database connection.

    This fixture connects to the database, verifies the connection,
    and ensures the connection is closed after all tests are complete.

    Yields:
        None: This fixture doesn't yield a value, just manages the connection
    """
    try:
        await connect_to_db()
        logger.info("Database connected successfully in setup_database fixture")
        # Verify database connection
        await database.execute("SELECT 1")
        logger.info("Database connection verified")
        yield
    finally:
        await disconnect_from_db()
        logger.info("Database disconnected in setup_database fixture")


def list_files_in_folder(folder_path):
    """List all files in a folder.

    Args:
        folder_path: Path to the folder to list files from

    Returns:
        list: List of filenames in the folder
    """
    try:
        files = os.listdir(folder_path)
        return files
    except FileNotFoundError:
        logger.info(f"The folder {folder_path} does not exist.")
        return []
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return []


def is_db_ready(database_url):
    """Check if the database is ready to accept connections.

    This function attempts to connect to the database multiple times,
    with a short delay between attempts, to allow for the database to
    become available.

    Args:
        database_url: The URL of the database to connect to

    Returns:
        bool: True if the database is ready, False otherwise
    """
    engine = create_engine(database_url)
    for _ in range(10):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database is ready to connect")
            return True
        except Exception as e:
            logger.info(f"Database is not ready yet: {e}")
            time.sleep(2)
    return False


@pytest.fixture(scope="session", autouse=True)
def run_liquibase():
    """Set up the database schema using Liquibase migrations.

    This fixture runs automatically for all tests in the session and ensures
    that the database schema is properly set up before any tests run.
    """
    changelog_file = "db/changelog.yaml"
    jdbc_driver_path = "lib/" + list_files_in_folder("lib")[0]
    logger.info(f"Running Liquibase migrations on {DATABASE_URL}")
    logger.info(
        f"Using changelog file: {changelog_file} and JDBC driver: {jdbc_driver_path}"
    )

    if not os.path.exists(changelog_file):
        logger.error(f"Changelog file not found: {changelog_file}")
        raise SystemExit("Exiting test suite due to missing changelog file")

    if not os.path.exists(jdbc_driver_path):
        logger.error(f"JDBC driver not found: {jdbc_driver_path}")
        raise SystemExit("Exiting test suite due to missing JDBC driver")

    if not is_db_ready(DATABASE_URL):
        logger.error("Database is not ready to connect")
        raise SystemExit("Exiting test suite due to database not being ready")

    logger.info("JDBC URL: %s", DATABASE_URL)
    jdbc_url = f"jdbc:postgresql://localhost:{PG_PORT}/test?user=test&password=test"
    logger.info("JDBC URL: %s", jdbc_url)

    liquibase_cmd = [
        "liquibase",
        "--classpath=" + jdbc_driver_path,
        "--url=" + jdbc_url,
        "--changeLogFile=" + changelog_file,
        "--driver=org.postgresql.Driver",
        "--log-level=debug",
        "update",
    ]
    logger.info(f"Running command: {' '.join(liquibase_cmd)}")
    try:
        result = subprocess.run(
            liquibase_cmd, check=True, capture_output=True, text=True
        )
        logger.info("Liquibase migrations completed successfully")
        logger.info("%s", result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Liquibase migrations failed with error: %s", e)
        logger.info("%s", e.stderr)
        logger.info("%s", e.output)
        raise SystemExit("Exiting test suite due to Liquibase migration failure")
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        logger.info("%s", e.stderr)
        logger.info("%s", e.output)
        raise SystemExit(
            "Exiting test suite due to unexpected error during Liquibase migration"
        )
    logger.info("Liquibase migrations completed successfully")


@pytest.fixture(scope="function")
def db_session():
    """Provide a database session for testing.

    Yields:
        SQLAlchemy session: A database session for test operations
    """
    # Use the same database URL as the application
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def test_client():
    """Test client."""
    # Create a fresh test client for each test
    with TestClient(app) as client:
        yield client


@pytest.mark.integration
def test_read_root_200(db_session, run_liquibase, setup_database, test_client):
    """Test that the root endpoint returns a 200 status code with a message from the database."""
    # First delete all existing messages
    query_delete = text("DELETE FROM messages")
    db_session.execute(query_delete)

    # Insert a specific test message
    test_message = "Hello, World! from IT test"
    query_insert = text(f"INSERT INTO messages (message) VALUES ('{test_message}')")
    db_session.execute(query_insert)
    db_session.commit()
    logger.info(f"Inserted message '{test_message}' into the database")

    # Shortened comment
    response = test_client.get("/")
    logger.info("Response from GET /: %s", response.json())
    assert response.status_code == 200
    assert response.json() == {"message": test_message}


@pytest.mark.integration
def test_read_root_404(db_session, run_liquibase, setup_database, test_client):
    """Test that the root endpoint returns a 404 status code when no messages are available."""
    query = text("DELETE FROM messages")
    db_session.execute(query)
    db_session.commit()

    logger.info("Deleted all messages from the database")
    response = test_client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No messages available"}


@pytest.mark.integration
def test_read_root_500(test_client):
    # Temporarily stop the container to simulate database failure
    try:
        container.stop()

        response = test_client.get("/")
        assert response.status_code == 500
        assert response.json() == {"detail": "Error fetching messages"}
    finally:
        # Ensure container is restarted for subsequent tests
        container.start()
        # Wait for container to be ready
        time.sleep(1)
