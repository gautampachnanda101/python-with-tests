# Python Web Application with FastAPI and PostgreSQL

A robust web application built with FastAPI and PostgreSQL, showcasing best practices for Python web development including integration testing, database migrations, and containerization.

## Overview

This application provides a simple REST API that serves random messages from a PostgreSQL database. The project demonstrates:

- FastAPI for building high-performance APIs
- PostgreSQL for data storage
- Liquibase for database migrations
- Comprehensive testing (unit and integration tests)
- Docker containerization
- Proper error handling and status codes

## Architecture

- **API Layer**: FastAPI handles HTTP requests and responses
- **Database Layer**: PostgreSQL stores messages that are served by the API
- **Migration Tool**: Liquibase manages database schema changes
- **Testing**: Pytest with testcontainers for integration testing

## Prerequisites

- Python 3.9+
- Poetry (dependency management)
- Docker and Docker Compose
- Liquibase
- PostgreSQL JDBC driver

## Installation

1. Clone the repository
2. Run the setup script to install dependencies:

```bash
./setup.sh
```

This will:
- Install required system dependencies (via Homebrew)
- Set up Poetry and install Python dependencies
- Download the PostgreSQL JDBC driver for Liquibase

## Running the Application

Start the application using:

```bash
./start.sh
```

Or using make:

```bash
make run
```

The application will be available at http://localhost:8000

## API Endpoints

- `GET /`: Returns a random message from the database
  - Returns 200 OK with a message if messages exist
  - Returns 404 Not Found if no messages exist
  - Returns 500 Internal Server Error if there's a database connection issue

## Testing

The project includes both unit tests and integration tests.

### Running All Tests

```bash
make test
```

This will:
1. Clean up any existing Docker containers and resources
2. Run unit tests
3. Run integration tests

### Running Unit Tests Only

```bash
make unit-test
```

### Running Integration Tests Only

```bash
make integration-test
```

### Test Architecture

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test the entire system with a real PostgreSQL database in a Docker container
  - Uses testcontainers to dynamically create and manage PostgreSQL containers
  - Automatically finds available ports to avoid conflicts
  - Properly cleans up resources after tests complete

## Development

### Project Structure

- `app/`: Application code
  - `main.py`: FastAPI application and endpoints
  - `pg.py`: Database connection management
- `db/`: Database migration files
  - `changelog.yaml`: Liquibase changelog for database schema
- `tests/`: Test files
  - `test_main.py`: Unit tests
  - `test_integration.py`: Integration tests
- `lib/`: External libraries (JDBC driver)
- `.gitignore`: Specifies intentionally untracked files to ignore

### Makefile Commands

- `make setup`: Set up the development environment
- `make run`: Run the application
- `make test`: Run all tests
- `make unit-test`: Run unit tests only
- `make integration-test`: Run integration tests only
- `make clean`: Clean up Docker containers and resources

## Troubleshooting

### Port Conflicts

If you encounter port conflicts when running tests or the application:

1. The integration tests now use dynamic port allocation to avoid conflicts
2. For manual troubleshooting, check for running containers:
   ```bash
   docker ps
   ```
3. Stop and remove conflicting containers:
   ```bash
   docker stop <container_id>
   docker rm <container_id>
   ```
4. Clean up all resources:
   ```bash
   make clean
   ```

### Database Connection Issues

If the application can't connect to the database:

1. Verify the PostgreSQL container is running:
   ```bash
   docker ps | grep postgres
   ```
2. Check the logs for connection errors:
   ```bash
   docker logs <container_id>
   ```
3. Verify the DB_URL environment variable is correctly set

## CI/CD Pipeline

This project includes a GitHub Actions workflow for continuous integration and continuous deployment. The workflow automatically runs on push to the main branch and on pull requests.

### CI/CD Pipeline Steps

1. **Test**:
   - Linting with Flake8
   - Code formatting check with Black
   - Import sorting check with isort
   - Tests with pytest and coverage reporting
   - Uses a PostgreSQL service container for integration tests

2. **Build and Push** (only on push to main):
   - Builds a Docker image
   - Pushes the image to Docker Hub
   - Tags with both latest and commit SHA
   - Uses Docker layer caching for faster builds

3. **Deploy** (only on push to main):
   - Connects to deployment server via SSH
   - Pulls the latest Docker image
   - Updates the running containers with zero downtime
   - Cleans up unused Docker resources

### Required Secrets

To use this workflow, you need to set up the following secrets in your GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token
- `DEPLOY_SERVER_HOST`: The hostname or IP of your deployment server
- `DEPLOY_SERVER_USER`: SSH username for the deployment server
- `DEPLOY_SERVER_KEY`: SSH private key for authentication

### Setting Up GitHub Actions

The workflow is already configured in `.github/workflows/ci-cd.yml`. When you push to GitHub, it will automatically run.

## Security Best Practices

### Environment Variables

- Never commit `.env` files or any files containing secrets to version control
- The `.gitignore` file is configured to exclude common secret files and directories
- Use environment variables for sensitive configuration (database credentials, API keys, etc.)
- For local development, create a `.env` file (which is ignored by git) with your environment variables

### Example .env File

Create a file named `.env` in the project root with the following variables (replace with your actual values):

```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
DB_URL=postgresql://your_username:your_password@localhost:5432/your_database
DRIVER_VERSION=42.7.3
```

### Secrets Management

- For production, use a secure secrets management solution (e.g., Kubernetes Secrets, AWS Secrets Manager)
- Rotate credentials regularly
- Use the principle of least privilege for database users

## License

This project is open source and available under the MIT License.
