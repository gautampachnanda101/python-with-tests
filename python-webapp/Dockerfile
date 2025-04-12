# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    openssl \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

# Verify Poetry installation
RUN poetry --version

# Copy the project files into the container
COPY . .
# Install Poetry dependencies
RUN poetry install --no-root && poetry add fastapi uvicorn databases asyncio sqlalchemy psycopg2-binary asyncpg httpx pytest testcontainers pytest-html urllib3 pytest-asyncio

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
