# Makefile for learningpython

# Variables
PYTHON = python3
PYTEST = poetry run pytest
PYTEST_ARGS = -v
COVERAGE = poetry run coverage
POETRY = poetry

# Default target
all: lint format test

# Install dependencies
install:
	$(POETRY) install

# Run tests
test:
	$(PYTEST) $(PYTEST_ARGS)

# Run tests with coverage
test-coverage:
	$(POETRY) run pytest --cov=org --cov-report=term-missing --cov-report=html --cov-fail-under=90

# Run a specific test module
test-module:
	$(PYTEST) $(PYTEST_ARGS) $(module)

# Run the calculator example
run-calculator:
	$(POETRY) run python -m org.pachnanda.learning.calculator_demo

# Format code with Black
format:
	$(POETRY) run black .

# Sort imports with isort
sort:
	$(POETRY) run isort .

# Lint code with Flake8
lint:
	$(POETRY) run flake8 .

# Format and lint code (spotless equivalent)
spotless: format sort lint

# Check code formatting without making changes
format-check:
	$(POETRY) run black --check .
	$(POETRY) run isort --check .

# Clean up generated files
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Initialize Poetry project (if not already initialized)
init:
	$(POETRY) init

# Add dependencies
add-dep:
	$(POETRY) add $(pkg)

# Add development dependencies
add-dev-dep:
	$(POETRY) add --group dev $(pkg)

.PHONY: all install test test-coverage test-module run-calculator clean init add-dep add-dev-dep format sort lint spotless format-check
