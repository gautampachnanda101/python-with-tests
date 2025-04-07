#!/bin/sh
brew update || brew upgrade
openssl --version | brew install openssl
python --version | brew install python
poetry --version | brew install poetry
poetry init --no-interaction
poetry install --no-root
poetry add fastapi uvicorn databases asyncio sqlalchemy psycopg2-binary asyncpg httpx pytest testcontainers pytest-html urllib3 pytest-asyncio
function fetch_driver() {
  source .env
  echo "Fetching PostgreSQL JDBC driver... for version $DRIVER_VERSION"
  DRIVER_JAR="postgresql-$DRIVER_VERSION.jar"
  DRIVER_PATH="./lib/postgresql-$DRIVER_VERSION.jar"
  # Check if the JDBC driver is missing and download it if necessary
  if [ ! -f "$JDBC_DRIVER_PATH" ]; then
    echo "PostgreSQL JDBC driver not found. Downloading..."
    mkdir -p ./lib || true
    curl -o "$DRIVER_PATH" "https://repo1.maven.org/maven2/org/postgresql/postgresql/${DRIVER_VERSION}/${DRIVER_JAR}"
    echo "PostgreSQL JDBC driver downloaded successfully."
  fi
}
fetch_driver