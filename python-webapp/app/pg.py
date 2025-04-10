"""PostgreSQL database connection module for the Python Web App.

This module handles database connections, providing functions to connect to
and disconnect from a PostgreSQL database. It uses the Database class from
the databases package to manage asynchronous database operations.
"""

import logging
import os

from databases import Database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read the database URL from the environment variable
DATABASE_URL = os.getenv("DB_URL")

# Print the database URL
print(f"DATABASE_URL environment variable: {DATABASE_URL}")

if not DATABASE_URL:
    logger.error("DB_URL environment variable is not set.")
    raise RuntimeError("DB_URL environment variable is not set.")

database = Database(DATABASE_URL)


async def connect_to_db():
    """Connect to the PostgreSQL database.

    This asynchronous function establishes a connection to the PostgreSQL database
    using the database URL specified in the DB_URL environment variable.

    Raises:
        Exception: If there is an error connecting to the database
    """
    try:
        await database.connect()
        logger.info("Database connected successfully.")
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        raise


async def disconnect_from_db():
    """Disconnect from the PostgreSQL database.

    This asynchronous function closes the connection to the PostgreSQL database.
    It should be called when the application is shutting down to ensure proper
    cleanup of database resources.

    Logs any errors that occur during disconnection but does not raise exceptions
    to avoid disrupting the shutdown process.
    """
    try:
        await database.disconnect()
        logger.info("Database disconnected successfully.")
    except Exception as e:
        logger.error(f"Error disconnecting from the database: {e}")
