# Python with Tests

This repository contains Python projects demonstrating best practices for testing, CI/CD, and project structure.

## Projects

### 1. Learning Python

A simple Python project demonstrating basic calculator operations with unit tests. This project uses Poetry for dependency management and includes code quality tools.

- [View Project](./learningpython/README.md)

### 2. Python Web App

A FastAPI web application with PostgreSQL database integration. Includes comprehensive integration tests using testcontainers.

- [View Project](./python-webapp/README.md)

## Features

- **Comprehensive Testing**: Unit tests and integration tests with high coverage requirements
- **CI/CD Pipelines**: GitHub Actions workflows for continuous integration and deployment
- **Code Quality Tools**: Black, isort, and Flake8 for consistent code style
- **Docker Integration**: Containerized applications and test environments
- **Documentation**: Detailed READMEs with setup and usage instructions

## Getting Started

Each project has its own README with detailed setup instructions. Navigate to the project directories to get started.

## Development

### Prerequisites

- Python 3.9 or higher
- Poetry (for the Learning Python project)
- Docker and Docker Compose (for the Python Web App)
- Make
- pre-commit (for code quality hooks)

### Common Commands

```bash
# Clone the repository
git clone https://github.com/yourusername/python-with-tests.git
cd python-with-tests

# Set up and run the Learning Python project
cd learningpython
make install
make test

# Set up and run the Python Web App
cd ../python-webapp
make setup
make run
```

## Code Quality Tools

### Pre-commit Hooks

This repository uses pre-commit hooks to ensure code quality standards are met before code is committed. The hooks automatically format code, check for syntax errors, and enforce style guidelines.

To set up the pre-commit hooks:

```bash
# Run the setup script
./setup-hooks.sh
```

The following hooks are configured:

- **Black**: Automatically formats Python code
- **isort**: Sorts and organizes imports
- **Flake8**: Checks for PEP 8 compliance and other code quality issues
- **MyPy**: Performs static type checking
- **General hooks**: Checks for trailing whitespace, merge conflicts, large files, etc.

You can manually run all hooks on all files with:

```bash
pre-commit run --all-files
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
