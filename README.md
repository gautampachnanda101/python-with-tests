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

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
