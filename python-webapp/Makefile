# Define variables
PYTHON = poetry run python
PYTEST = poetry run pytest
DOCKER_COMPOSE = docker-compose
TESTCONTAINERS = testcontainers
setup:
	./setup.sh
run: clean setup
	./start.sh
test:
	./test.sh
#clean:
#	./clean.sh

# Define variables
PYTHON = poetry run python
PYTEST = poetry run pytest
DOCKER_COMPOSE = docker-compose
TESTCONTAINERS = testcontainers

# Default target
all: test

# Install dependencies
install:
	poetry install

# Run unit tests
unit-test:
	$(PYTEST) -m "not integration" --html=report.html

# Run integration tests
integration-test:
	$(PYTEST) -m "integration" --html=report.html --log-cli-level=DEBUG

# Run all tests
test: clean unit-test integration-test
	@echo "All tests completed successfully!"

# Start test containers
start-test-containers:
	$(DOCKER_COMPOSE) -f docker-compose.test.yml up -d

# Stop and remove test containers
stop-test-containers:
	$(DOCKER_COMPOSE) -f docker-compose.test.yml down --remove-orphans

# Clean up
clean:
	@echo "Cleaning up Docker resources..."
	-docker ps -a -q --filter "name=postgres" | xargs -r docker stop
	-docker ps -a -q --filter "name=postgres" | xargs -r docker rm
	-$(DOCKER_COMPOSE) down --remove-orphans 2>/dev/null || true
	-docker volume prune -f --all 2>/dev/null || true
	@echo "Cleaning up Python cache..."
	-rm -rf __pycache__
	-find . -name "__pycache__" -type d -exec rm -rf {} +
	-find . -name "*.pyc" -delete

# Run tests with test containers
test-with-containers: clean start-test-containers test stop-test-containers

.PHONY: all install unit-test integration-test test start-test-containers stop-test-containers clean test-with-containers
