import random
import logging
from fastapi import FastAPI, HTTPException
from .pg import database, connect_to_db, disconnect_from_db

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_from_db()

@app.get("/")
async def read_root():
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