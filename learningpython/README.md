# Learning Python

A simple Python project demonstrating basic calculator operations with unit tests. This project uses Poetry for dependency management.

## Project Structure

```
learningpython/
├── Makefile               # Commands to run tests and code
├── README.md              # This file
├── pyproject.toml         # Poetry configuration and dependencies
└── org/
    └── pachnanda/
        ├── learning/
        │   ├── calculator.py      # Calculator implementation
        │   └── calculator_demo.py # Demo script
        └── test/
            └── test_calculator.py # Unit tests
```

## Prerequisites

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

## Setup

1. Install Poetry (if not already installed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:

```bash
make install
```

This will create a virtual environment and install all required dependencies automatically.

## Running Tests

Run all tests:

```bash
make test
```

Run tests with coverage:

```bash
make test-coverage
```

Run a specific test module:

```bash
make test-module module=org/pachnanda/test/test_calculator.py
```

## Running the Calculator Demo

```bash
make run-calculator
```

## Cleaning Up

Remove generated files (cache, coverage reports, etc.):

```bash
make clean
```

## Available Make Commands

- `make install`: Install dependencies using Poetry
- `make test`: Run all tests
- `make test-coverage`: Run tests with coverage reporting (fails if coverage < 90%)
- `make test-module module=<path>`: Run a specific test module
- `make run-calculator`: Run the calculator demo
- `make format`: Format code using Black
- `make sort`: Sort imports using isort
- `make lint`: Lint code using Flake8
- `make spotless`: Run all code style tools (format, sort, lint)
- `make format-check`: Check code formatting without making changes
- `make clean`: Clean up generated files
- `make init`: Initialize a new Poetry project (rarely needed)
- `make add-dep pkg=<package>`: Add a new dependency
- `make add-dev-dep pkg=<package>`: Add a new development dependency

## CI/CD Pipeline

This project includes a GitHub Actions workflow for continuous integration and delivery. The workflow automatically runs on push to the main branch and on pull requests.

### CI Pipeline Steps

1. **Test**: Runs on multiple Python versions (3.9, 3.10, 3.11)
   - Linting with Flake8
   - Code formatting check with Black
   - Import sorting check with isort
   - Tests with pytest and coverage reporting
   - Coverage upload to Codecov

2. **Build**: Runs after tests pass
   - Builds the Python package
   - Archives the distribution files as artifacts

### Setting Up GitHub Actions

The workflow is already configured in `.github/workflows/ci.yml`. When you push to GitHub, it will automatically run.

## Code Quality Tools

This project uses several tools to ensure code quality:

### Code Style

- **Black**: An opinionated code formatter that ensures consistent code style
- **isort**: Automatically sorts and formats imports
- **Flake8**: A code linter that checks for style and potential errors

You can run all code style tools at once with:

```bash
make spotless
```

### Test Coverage

The project is configured to require at least 90% test coverage. You can check the current coverage with:

```bash
make test-coverage
```

This will generate an HTML report in the `htmlcov` directory that you can open in a browser to see detailed coverage information.

## Managing Dependencies with Poetry

This project uses Poetry for dependency management. Here are some common Poetry commands:

```bash
# Activate the Poetry shell (virtual environment)
poetry shell

# Add a new dependency
poetry add <package>

# Add a development dependency
poetry add --group dev <package>

# Update dependencies
poetry update

# Show installed dependencies
poetry show
```

For more information, see the [Poetry documentation](https://python-poetry.org/docs/).
