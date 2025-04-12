"""Main application module for the Python Web App.

This module defines the FastAPI application, its routes, and event handlers.
It provides a simple API that returns random messages from a database.
"""

import logging
import random

from fastapi import FastAPI, HTTPException

from .pg import connect_to_db, database, disconnect_from_db

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Connect to the database when the application starts.

    This function is automatically called when the FastAPI application starts.
    It establishes a connection to the database using the connect_to_db function.
    """
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from the database when the application shuts down.

    This function is automatically called when the FastAPI application shuts down.
    It closes the database connection using the disconnect_from_db function.
    """
    await disconnect_from_db()


@app.get("/")
async def read_root():
    """Handle GET requests to the root endpoint.

    This function retrieves a random message from the database and returns it.

    Returns:
        dict: A dictionary containing a random message from the database

    Raises:
        HTTPException: If no messages are available (404) or if there's an error
                      fetching messages from the database (500)
    """
    try:
        query = "SELECT message FROM messages"
        messages = await database.fetch_all(query=query)
        if not messages:
            # Return 404 directly without going through the exception handler
            raise HTTPException(status_code=404, detail="No messages available")
        message = random.choice(messages)["message"]
        return {"message": message}
    except HTTPException:
        # Re-raise HTTP exceptions without changing them
        raise
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        raise HTTPException(status_code=500, detail="Error fetching messages")
