import os
import logging
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
    try:
        await database.connect()
        logger.info("Database connected successfully.")
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        raise

async def disconnect_from_db():
    try:
        await database.disconnect()
        logger.info("Database disconnected successfully.")
    except Exception as e:
        logger.error(f"Error disconnecting from the database: {e}")