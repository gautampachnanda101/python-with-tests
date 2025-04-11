#!/bin/sh
set -e
source .env
# Define the path to the JDBC driver
JDBC_DRIVER_PATH="./lib/"
DRIVER_PATH="./lib/postgresql-$DRIVER_VERSION.jar"
# Check if the JDBC driver is missing and download it if necessary
#if [ ! -f "$JDBC_DRIVER_PATH" ]; then
#  echo "PostgreSQL JDBC driver not found. Downloading..."
#  mkdir -p ./lib
#  curl -o "$JDBC_DRIVER_PATH" https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.23/postgresql-42.7.3.jar
#fi

# Kill any application running on port 5432
if lsof -i:5432 -t >/dev/null; then
  echo "Killing application running on port 5432..."
  kill -9 $(lsof -i:5432 -t)
fi

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)
DATABASE_URL="jdbc:postgresql://$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
DATABASE_USER="$POSTGRES_USER"
DATABASE_PASSWORD="$POSTGRES_PASSWORD"

# Stop and remove any existing containers
docker-compose down --remove-orphans || true

# Start PostgreSQL using Docker Compose
docker-compose up -d

# Wait for PostgreSQL to be ready with a timeout
echo "Waiting for PostgreSQL to be ready..."
timeout=60
while ! docker exec postgres_db pg_isready -U "$DATABASE_USER"; do
  timeout=$((timeout - 1))
  if [ $timeout -le 0 ]; then
    echo "PostgreSQL is not ready. Exiting script."
    exit 1
  fi
  sleep 1
  echo "Waiting for PostgreSQL to be ready..."
done
echo "PostgreSQL is ready."

echo "Checking database connection..."
# Check if the database connection is working
if ! liquibase --classpath=$DRIVER_PATH --url=$DATABASE_URL --username=$DATABASE_USER --password=$DATABASE_PASSWORD --changeLogFile=./db/changelog.yaml --driver=org.postgresql.Driver --log-level debug status; then
  echo "Database connection failed. Exiting script."
  exit 1
fi
echo "Database connection is working."

echo "Applying database migrations... to $DATABASE_URL"
# Run Liquibase to update the database schema
if ! liquibase --classpath=$DRIVER_PATH --url=$DATABASE_URL --username=$DATABASE_USER --password=$DATABASE_PASSWORD --changeLogFile=./db/changelog.yaml --driver=org.postgresql.Driver --log-level debug update; then
  echo "Liquibase update failed. Exiting script."
  exit 1
fi

echo "Database migrations applied. Starting application..."
# Start the FastAPI application
poetry run uvicorn app.main:app --reload
